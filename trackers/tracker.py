import cv2
import numpy as np
from team_assigner.team_assigner import TeamAssigner
from map_creator.map_creator import MapCreator

class Tracker:
    def __init__(self, model, video_path, output_path):
        self.model = model
        self.video_path = video_path
        self.output_path = output_path
        # Store class and team information for each tracked object
        self.id_to_class = {}
        self.id_to_team = {}
        self.team_assigner = TeamAssigner()
        self.team_colors = {}
        # Initialize field map for visualization
        self.map_creator = MapCreator(map_width=400, map_height=250)
        # Ball tracking for position interpolation
        self.ball_last_position = None
        self.ball_position_history = []

    def get_color_for_class(self, class_name):
        """Define colors for different object classes"""
        CLASS_COLORS = {
            "player": (255, 255, 255),      # White for players
            "referee": (0, 255, 255),       # Yellow for referees
            "ball": (255, 0, 255)           # Magenta for ball
        }
        return CLASS_COLORS.get(class_name, (0, 255, 0))

    def track(self, cap, out):
        """Main tracking loop - processes each frame of the video"""
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Run YOLO detection with tracking enabled
            results = self.model.track(frame, persist=True, tracker="bytetrack.yaml")

            if results[0].boxes is None:
                out.write(frame)
                continue

            # Extract detection results
            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.id is not None else []
            class_ids = results[0].boxes.cls.cpu().numpy()
            names = self.model.names

            # First pass: collect all players for team assignment
            player_detections = {}
            for box, track_id, cls_id in zip(boxes, ids, class_ids):
                class_name = names[int(cls_id)].lower()
                if class_name == "player":
                    player_detections[track_id] = {'bbox': box}

            # Assign teams based on shirt colors
            if len(player_detections) > 0:
                self.team_assigner.assign_teams(frame, player_detections)
            
            # Reset field map for new frame
            self.map_creator.reset_map()

            ball_detected = False
            # Second pass: process all detections and draw visualizations
            for box, track_id, cls_id in zip(boxes, ids, class_ids):
                x1, y1, x2, y2 = map(int, box)
                cx = int((x1 + x2) / 2)  # Center X coordinate
                cy = int(y2)              # Bottom Y coordinate (feet position)
                class_name = names[int(cls_id)].lower()

                # Preserve class info per ID across frames
                if track_id in self.id_to_class:
                    class_name = self.id_to_class[track_id]
                else:
                    self.id_to_class[track_id] = class_name

                # Handle player detection and team assignment
                if class_name == "player":
                    team_id = self.team_assigner.get_player_team(frame, box, track_id)
                    self.id_to_team[track_id] = team_id

                    # Set team colors: Blue for team 1, Red for team 2
                    color = (255, 0, 0) if team_id == 1 else (0, 0, 255)
                    
                    # Draw player position on field map
                    map_x = int(cx * self.map_creator.map_width / frame.shape[1])
                    map_y = int(cy * self.map_creator.map_height / frame.shape[0])
                    self.map_creator.draw_player(map_x, map_y, color)
                elif class_name == "ball":
                    ball_detected = True
                    self.ball_last_position = (cx, cy)
                    self.ball_position_history.append((cx, cy))
                    # Draw ball position on field map
                    map_x = int(cx * self.map_creator.map_width / frame.shape[1])
                    map_y = int(cy * self.map_creator.map_height / frame.shape[0])
                    self.map_creator.draw_ball(map_x, map_y)
                    color = self.get_color_for_class(class_name)
                else:
                    color = self.get_color_for_class(class_name)

                # Scale ellipse size based on bounding box dimensions
                box_width = x2 - x1
                box_height = y2 - y1

                ellipse_width = int(box_width * 0.5)
                ellipse_height = int(box_height * 0.15)

                # Set minimum ellipse dimensions
                ellipse_width = max(15, ellipse_width)
                ellipse_height = max(5, ellipse_height)

                # Draw elliptical bounding box around detected objects
                cv2.ellipse(
                    frame,
                    (cx, cy),
                    (ellipse_width, ellipse_height),
                    0, -45, 235,  # Angle parameters for partial ellipse
                    color, 2, lineType=cv2.LINE_4
                )

                # Add arrow above ball for better visibility
                if class_name == "ball":
                    arrow_start = (cx, cy - 15)
                    arrow_end = (cx, cy - 30)
                    cv2.arrowedLine(frame, arrow_start, arrow_end, color, 2, tipLength=0.4)

                # Create label with object info and team assignment
                team_info = f" | T{self.id_to_team[track_id]}" if track_id in self.id_to_team and class_name == "player" else ""
                label = f"{class_name} | ID:{int(track_id)}{team_info}"

                # Draw background rectangle for text
                text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
                cv2.rectangle(frame,
                              (cx - text_size[0] // 2 - 5, cy + 14),
                              (cx + text_size[0] // 2 + 5, cy + 34),
                              color, -1)
                # Draw text label
                cv2.putText(frame, label,
                            (cx - text_size[0] // 2, cy + 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.55, (0, 0, 0), 2)

            # Ball position interpolation when ball is not detected
            if not ball_detected and self.ball_last_position is not None:
                if len(self.ball_position_history) > 1:
                    # Simple linear interpolation based on previous positions
                    last_pos = self.ball_position_history[-1]
                    second_last_pos = self.ball_position_history[-2]
                    dx = last_pos[0] - second_last_pos[0]
                    dy = last_pos[1] - second_last_pos[1]
                    interpolated_pos = (last_pos[0] + dx, last_pos[1] + dy)
                    self.ball_last_position = interpolated_pos
                    self.ball_position_history.append(interpolated_pos)
                
                # Draw interpolated ball position on map
                cx, cy = self.ball_last_position
                map_x = int(cx * self.map_creator.map_width / frame.shape[1])
                map_y = int(cy * self.map_creator.map_height / frame.shape[0])
                self.map_creator.draw_ball(map_x, map_y)

            # Overlay the field map on the video frame
            map_image = self.map_creator.get_map()
            frame[10:10+map_image.shape[0], 10:10+map_image.shape[1]] = map_image

            out.write(frame)

        out.release()
        cap.release()
