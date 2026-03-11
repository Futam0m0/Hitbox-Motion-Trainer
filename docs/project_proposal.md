**Project Title:**
Hitbox Motion Training Tracker

---

# 1. Project Problem Domain

Fighting games require precise and consistent execution of directional motions such as quarter-circle forward (QCF), dragon punch (DP), and half-circle inputs. These motions must be performed within very short timing windows to execute special moves successfully.

Players who switch to a hitbox-style controller often experience difficulty adapting to the new input method because it requires different finger coordination compared to traditional arcade sticks or gamepads.

Currently, most training modes in fighting games do not provide detailed analytics on player input execution, such as motion consistency, execution speed, or success rates over time.

This project aims to develop a **Hitbox Motion Training Tracker**, a system that records directional inputs from a hitbox controller and analyzes motion patterns such as QCF, DP, and other common fighting game inputs. The system stores motion attempts and training sessions in a database and allows players to review performance statistics.

The system will help players track their training progress and improve execution consistency when learning hitbox controls.

---

# 2. Enterprise Requirements and User Roles

The system simulates a small-scale analytics platform for player training data.

**User Roles**

**Player**

* Uses the hitbox controller to perform motion inputs during training sessions.
* Views statistics related to motion success rate, execution speed, and practice frequency.

**System Administrator**

* Defines motion patterns to be tracked (e.g., DP, QCF, QCB).
* Manages motion definitions and system configuration.

Although the system is primarily designed for individual use, the architecture supports storing multiple players and sessions.

---

# 3. Functional Specifications and Related Data

The system performs the following main functions:

1. **Input Recording**

   * Detects directional button inputs from the hitbox controller connected to the computer.

2. **Motion Detection**

   * Analyzes sequences of directional inputs to determine whether a predefined motion pattern (e.g., QCF or DP) has been performed.

3. **Session Tracking**

   * Groups motion attempts into training sessions.

4. **Performance Analytics**

   * Calculates statistics such as:

     * success rate of motion execution
     * fastest execution time
     * total attempts per motion
     * training duration

5. **Data Storage**

   * All input events, motion attempts, and session data are stored in a relational database.

**Main Data Entities**

The system will manage the following data:

* Player
* Training Session
* Motion Definition
* Motion Attempt
* Input Event

These entities will later be modeled using an **Entity-Relationship Diagram (ERD)**.

---

# 4. Project Schedule and Milestones

| Week   | Milestone                                  |
| ------ | ------------------------------------------ |
| Week 1 | Project proposal submission                |
| Week 2 | Requirement analysis and system design     |
| Week 3 | Entity-Relationship diagram development    |
| Week 4 | Relational schema and normalization        |
| Week 5 | Database implementation using SQL          |
| Week 6 | Development of input logging module        |
| Week 7 | Motion detection implementation            |
| Week 8 | Data analysis queries and system testing   |
| Week 9 | Final documentation and project submission |

---

# 5. Tools for Design and Development

The following tools will be used in this project:

**Database System**

* Microsoft SQL Server

**Programming Language**

* Python

**Development Environment**

* Visual Studio Code

**Controller Hardware**

* Hitbox controller using a Tachyon Black Plus PCB

**Design Tools**

* ER diagram design tools such as Draw.io or Lucidchart

These tools will support the development of the system, data storage, and analysis of motion execution data.
