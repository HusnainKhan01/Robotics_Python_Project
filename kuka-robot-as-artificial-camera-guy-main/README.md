# kuka-robot-as-camera-guy

## Artificial Camera Guy
---
### Base Goals:

- Camera must detect face within a reasonable range (left/right, down/up, far/near).
Movement must be smoothed using any (one) method.
- Prepare two setups, run experiments and compare them in a scientific manner. 
- **Pick one of these:**
    1. **Network**: Communication via OpenShowVar (KUKA VAR PROXY) vs. XML via TCP/IP (KRLethernet)
    2. **Camera**: Mounted on the robot wrist vs. located in a fixed location.

### Extended Goals:

- Try various methods for smoothing movement (e.g. n frames fixed average, n frames moving average, n frames moving median,...), compare them in a scientific manner.
- Use a depth-sensor (lidar or structured light, available in the Lab) or infer from the detected face size. Move the robot accordingly.
- Compare both setups mentioned in the base goals.


### Document for safety workspace:
	- in PDF, KUKA System Software
	- KUKA System Software 8.3 (KSS_83_SI_en.pdf)
	- Operating and Programming Instructions for System Integrators
	- ### 6.11 Configuring workspaces
	- In KRC - controller:
	-- Step 1 - Determine Limits:
		Menu button(on top, a button with robot symbol) -> Display -> Actual position  -> axis- specific
		Rotate/move all axis and determined project specific limits and note down values
		
	-- Step 2: Configuring the workspace:
		Menu -> Configuration -> Miscellenious -> Workspace monitoring -> configuration -> axis-specific -> 
			Enter name: "cameraguy"
			put all the axis values (noted from step 1)
			Mode: "OUTSIDE_STOP"
		Save

### KRC usage:

	- Navigator -> R1 -> Program -> select robodkSync -> click on select below
	- Now, press and hold on forward play button (green color) on KRC display on top -> until program path is reached (in case of notification messages, select "confirm all" or "ok")
	- Press and hold again and is running