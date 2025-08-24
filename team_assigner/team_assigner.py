from sklearn.cluster import KMeans
import numpy as np
import cv2

class TeamAssigner:
    def __init__(self):
        self.team_colors = {}
        self.player_team_dict = {}
        self.kmeans = None

    def get_clustering_model(self, image):
        """Runs KMeans clustering on a cropped player image to identify dominant colors"""
        image_2d = image.reshape((-1, 3))
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=10, random_state=42)
        kmeans.fit(image_2d)
        return kmeans

    def get_player_color(self, frame, bbox):
        """Extracts dominant player shirt color from bounding box area"""
        # Crop the player region from the frame
        image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

        # Focus on top half of player (shirt area, ignore shorts & grass at bottom)
        top_half = image[0:int(image.shape[0] / 2), :]

        # Convert to HSV color space to reduce grass influence
        hsv = cv2.cvtColor(top_half, cv2.COLOR_BGR2HSV)
        # Create mask to remove low saturation pixels (grass / shadows)
        mask = hsv[:, :, 1] > 40   
        valid_pixels = top_half[mask]

        # Fallback to raw top_half if mask removes everything
        if valid_pixels.size == 0:
            valid_pixels = top_half.reshape(-1, 3)

        kmeans = self.get_clustering_model(valid_pixels)

        # Assign cluster with less green as player shirt color
        labels = kmeans.labels_
        clustered_img = labels.reshape(valid_pixels.shape[0], 1)

        # Check corners of original top_half cluster image to detect background
        clustered_image = labels.reshape(valid_pixels.shape[0], 1)
        corner_clusters = [labels[0], labels[-1]]
        # Determine which cluster represents the background
        non_player_cluster = max(set(corner_clusters), key=corner_clusters.count)
        player_cluster = 1 - non_player_cluster

        player_color = kmeans.cluster_centers_[player_cluster]
        return player_color

    def assign_teams(self, frame, player_detections):
        """Clusters all players into two teams based on shirt color similarity"""
        player_colors = []
        unassigned_players = []

        # Extract colors for all unassigned players
        for player_id, player_detection in player_detections.items():
            if player_id not in self.player_team_dict:
                bbox = player_detection['bbox']
                player_color = self.get_player_color(frame, bbox)
                player_colors.append(player_color)
                unassigned_players.append(player_id)

        if not unassigned_players:
            return

        player_colors = np.array(player_colors)

        # Use KMeans to cluster players into 2 teams
        if self.kmeans is None:
            self.kmeans = KMeans(n_clusters=2, init="k-means++", n_init=10, random_state=42)
            self.kmeans.fit(player_colors.reshape(-1, 3))
            # Store team color centroids
            self.team_colors[1] = self.kmeans.cluster_centers_[0]
            self.team_colors[2] = self.kmeans.cluster_centers_[1]

        # Assign team IDs to each player
        for i, player_id in enumerate(unassigned_players):
            team_id = self.kmeans.predict(player_colors[i].reshape(1, -1))[0]
            team_id += 1  # Convert 0/1 → 1/2 for team numbering
            self.player_team_dict[player_id] = team_id

    def get_player_team(self, frame, player_bbox, player_id):
        """Returns the assigned team ID for a given player"""
        return self.player_team_dict.get(player_id)
