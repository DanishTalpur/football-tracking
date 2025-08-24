<<<<<<< HEAD
# football-tracking
Football player tracking system using YOLO, OpenCV, and KMeans clustering.
=======
# Football Player Detection and Tracking

A computer vision project that detects and tracks football players in video footage using YOLO (You Only Look Once) object detection and custom tracking algorithms.

## 🚀 Features

- **Player Detection**: Uses YOLOv8 model trained on football player datasets
- **Player Tracking**: Custom tracking algorithm for consistent player identification across frames
- **Team Assignment**: Intelligent team assignment based on player positions and movements
- **Map Creation**: Generates field maps showing player positions and movements
- **Video Processing**: Processes video files and outputs annotated videos with tracking results

## 📋 Requirements

- Python 3.8+
- CUDA-compatible GPU (recommended for faster processing)
- See `requirements.txt` for detailed dependencies

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd Football
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download pre-trained models:**
   - Place your trained YOLO model in the `model/` directory
   - Or use the provided `best.pt` model from training results

## 📁 Project Structure

```
Football/
├── main.py                 # Main execution script
├── main.ipynb             # Jupyter notebook for experimentation
├── utils/                  # Utility functions
│   ├── bbox_utils.py      # Bounding box utilities
│   └── video_utils.py     # Video processing utilities
├── trackers/               # Tracking algorithms
│   └── tracker.py         # Main tracker implementation
├── map_creator/            # Field map generation
├── team_assigner/          # Team assignment logic
├── training/               # Training data and configurations
└── model/                  # Pre-trained models
```

## 🎯 Usage

### Basic Usage

1. **Run the main script:**
   ```bash
   python main.py
   ```

2. **Use Jupyter notebook:**
   ```bash
   jupyter notebook main.ipynb
   ```

### Customization

- Modify `main.py` to change input video path and output settings
- Adjust tracking parameters in `trackers/tracker.py`
- Customize team assignment logic in `team_assigner/team_assigner.py`

## 🔧 Configuration

The project uses several configuration options:

- **Model Path**: Update the model path in `main.py` to use your trained model
- **Video Path**: Change the input video path in `main.py`
- **Output Settings**: Modify output video format and quality settings

## 📊 Training

To train your own model:

1. Prepare your dataset in YOLO format
2. Update the `data.yaml` configuration file
3. Run training using Ultralytics:
   ```bash
   yolo train data=data.yaml model=yolov8n.pt epochs=100
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLOv8 implementation
- [OpenCV](https://opencv.org/) for computer vision utilities
- Football dataset contributors for training data

## 📞 Support

If you encounter any issues or have questions:

1. Check the existing issues in the repository
2. Create a new issue with detailed description
3. Include error messages and system information

---

**Note**: This project requires significant computational resources for video processing. Consider using GPU acceleration for better performance.
>>>>>>> cd603c1 (Initial commit - Football tracking project)
