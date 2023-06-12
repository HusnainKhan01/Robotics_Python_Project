# Face Detection new working with moving frames(with Queue)
def face_detection():
    # fpsLimit = 0.001 # throttle limit
    # startTime = time.time()
    # cv = cv2.VideoCapture(0)
    outer_count = 0
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(1)
    All_Faces = []
    imageRcvdValue = 0
    readingIsReady = False
    while not readingIsReady:
        count = 0
        # Read the frame
        _, img = cap.read()
        # kernel = np.ones((5, 5), np.float32) / 25
        # img = cv2.filter2D(img, -1, kernel)
        # img = cv2.blur(img, (5, 5))
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # gray = highPassFiltering(gray, 50)

        # Detect the faces
        # faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        faces = face_cascade.detectMultiScale(image=gray, scaleFactor=1.1, minNeighbors=4, minSize=(50, 50))
        new_X = 0
        new_Y = 0
        new_W = 0
        new_H = 0

        # Draw the rectangle around each face
        oneFaceDetected = False
        for (x, y, w, h) in faces:
            if not oneFaceDetected:
                oneFaceDetected = True
                new_X += x
                new_Y += y
                new_W += w
                new_H += h
                # Number of faces detected
                count += 1
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
            # print(faces)

        # Check if there is a face in the frame
        if count != 0:
            new_X = int(new_X / count)
            new_Y = int(new_Y / count)
            new_W = int(new_W / count)
            new_H = int(new_H / count)

            All_Faces.append([new_X, new_Y, new_W, new_H])
            imageRcvdValue += 1

            # TODO: make a check if the count reaches to 100 values then set the mean value of the face
            global count_For_All_Faces
            global IsFirstIteration

            if not IsFirstIteration:
                del All_Faces[0]

            if not IsFirstIteration or imageRcvdValue >= count_For_All_Faces:
                # calculate the mean value
                values = calculate_Mean(All_Faces)
                # cv2.rectangle(img, (new_X, new_Y), (new_X + new_W, new_Y + new_H), (255, 0, 255), 2)
                cv2.rectangle(img, (values[0], values[1]), (values[0] + values[2], values[1] + values[3]),
                              (255, 0, 255), 2)

                ######################################
                toMove = createCircle(values, img)
                print("coordinates sent from camera")
                print(toMove)
                readingIsReady = False
                yield toMove
                ######################################
                # TODO: Create object of Robot class
                # call maethod to move to the values returned by createCircle method
                # yield and design-pattern:generator
                ######################################

                # center_coordinates = (get_Center(values))
                # radius = 10
                # color = (255, 0, 0)
                # thickness = -1
                # cv2.circle(img, center_coordinates, radius, color, thickness)
                ######################################
                imageRcvdValue = 0

                IsFirstIteration = False

                # All_Faces = []

        # Display
        cv2.imshow('img', img)
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    return toMove