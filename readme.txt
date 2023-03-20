# ECS273-Winter2023 Final Project
Professor: Kwan-Liu Ma

TA: Yun-Hsin Kuo

Working Group: Yifeng Shi, Musheng He


## User Instructions
We implemented this project based on the template provided by instructors for the warmup programming
assignment, so there is no extra instructions need to be executed, just the original instructions introduced
in the template git repository in directory '/Assignment/README.md'

#### Quick Start
1. Run the  `./Inplementation/server/app.py` file.

2. Start the application, under `./Inplementation/dashboard` directory, by executing the following script:
   ```bash
   npm run start
   ```
   then, you can then visit `localhost:3000` in the browser to see the interface.

## Functionalities
1. Temporal force-directed graph to express the directed graph of Bitcoin signed weighted network.
   - A scroll bar to choose time.
   - Group nodes by pre-set conditions
   - As scroll bar to choose the value of gradient to indicate the number of groups users want to have.
   Interaction: Zoom in and out, drag, hover pointer on a node.
2. A stacked bar chart displaying the user degree distribution in the time unit of day.
   Furthermore, hovering pointer on a bar to see detailed text.
3. The contrast between in-degree and out-degree of each user shown in a scatter plot graph with grid.
   zoom in or drag to focus on interested areas, hover pointer on a plot to see text.
4. Two histograms displaying distribution of rating scores and frequency.
   hover pointer on a plot to see text.

Graphs described in 2. 3. and 4 are cascaded with the force-directed graph by hovering pointer on a particular node.
