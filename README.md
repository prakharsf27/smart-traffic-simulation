Smart Traffic Signal Simulation 🚦

An AI-based smart traffic signal simulation built using Python and Pygame.
The system compares traditional fixed-time traffic signals with adaptive AI traffic signals that dynamically adjust based on vehicle density.

⸻

📌 Project Overview

Urban traffic congestion is a major challenge in modern cities. Traditional traffic signals operate on fixed timers and do not adapt to real-time traffic conditions.

This project simulates an AI-based adaptive traffic signal controller that:
	•	Detects vehicle density near intersections
	•	Dynamically adjusts green light duration
	•	Prioritizes lanes with higher traffic
	•	Compares performance against fixed-time signals

The simulation visually demonstrates traffic flow and measures vehicle crossing time under both signal strategies.

⸻

🚀 Features
	•	🚦 AI Adaptive Traffic Signals
	•	⏱ Traditional Fixed-Timer Signals
	•	🚗 Vehicle density detection near intersections
	•	🏙 Multi-intersection smart city simulation
	•	📊 Performance comparison graph (AI vs Fixed)
	•	🚑 Emergency vehicle priority support
	•	🎮 Real-time simulation using Pygame

⸻

🧠 AI Traffic Signal Logic

The AI traffic controller uses traffic density detection to determine signal behavior.

Steps:
	1.	Detect vehicles approaching an intersection.
	2.	Count vehicles in each direction (North-South vs East-West).
	3.	Calculate traffic pressure.
	4.	Dynamically adjust green signal duration.
	5.	Prioritize directions with higher traffic.

This adaptive approach helps reduce:
	•	Traffic congestion
	•	Vehicle waiting time
	•	Idle engine time

⸻

🛠 Technologies Used
	•	Python 3
	•	Pygame – Real-time traffic simulation
	•	Matplotlib – Performance visualization
	•	Git & GitHub – Version control and collaboration

⸻

📊 Performance Comparison

The simulator runs two scenarios:
	1.	Fixed Traffic Signals
	2.	AI Adaptive Traffic Signals

After both simulations finish, a graph is generated showing:

Vehicle Time to Cross Intersection

Lower values indicate better traffic flow.

⸻

▶️ How to Run the Simulation

1️⃣ Install dependencies

pip install pygame matplotlib

2️⃣ Run the program

python twoway_simulation.py

3️⃣ Simulation flow
	1.	Fixed signal simulation runs
	2.	AI adaptive signal simulation runs
	3.	Graph comparing performance is displayed

⸻

📂 Project Structure

smart-traffic-simulation/
│
├── twoway_simulation.py   # Main simulation code
├── README.md              # Project documentation


⸻

👥 Team Collaboration

This repository is shared with the project team for development and improvements.

Team members can clone the repository using:

git clone https://github.com/prakharsf27/smart-traffic-simulation.git


⸻

📈 Future Improvements

Possible enhancements:
	•	Computer vision traffic detection (YOLO)
	•	Reinforcement learning traffic control
	•	Multi-lane road simulation
	•	Pedestrian crossings
	•	Traffic congestion heatmaps
	•	Real-world traffic dataset integration

⸻

🎓 Academic Purpose

This project was developed as part of a college design project to demonstrate how AI-based traffic control systems can improve urban traffic efficiency.

⸻

📜 License

This project is for educational purposes.
:::

⸻
