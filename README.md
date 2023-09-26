# Hand Gesture based Personal Assistant - (HAGPASS)

Hagpass is a computer vision based project that lets you perform action like opening files, folders, images, browser etc on your PC. It also lets you take Screenshots and control the PC volume and brightness - all that, using just hand gestures.

The gestures are a mix of ASL hand signs for alphabets and some custom hand symbols
You can find the dataset [here](https://www.kaggle.com/datasets/avishkararjan/personal-assistant-hand-signs-data)

## So how does it work ?
* The tool initially detects whether the within the frame is left or right
* Due to the high variety of actions that can be performed by using the tool, the tool uses 2 seperately trained models for the left and right hand - with a fix set of signs/gestures for each hand. See ![here](./left_n_right_segregation.txt "Gestures for each hand - compare with the dataset")
* Once the hand is detected, the respective model predicts the sign/gesture and carries out the action
* A short time-delay is added near the execution of the action - to prevent the action executing multiple times in a single instance, during the time taken by the hand to stop posing the gesture

The following are the sources of knowledge and inspiration that helped me build this project successfully-
1. [CVZone](https://www.computervision.zone/)
2. [Hand Detection](https://www.youtube.com/watch?v=1WPrGSnS7Qw)
3. [Teachable Machine](https://teachablemachine.withgoogle.com/)

