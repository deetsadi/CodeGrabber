    # cropped_contours, hier = cv2.findContours(cropped_thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    # for c in contours:
    #     # get the bounding rect
    #     x, y, w, h = cv2.boundingRect(c)
    #     # draw a white rectangle to visualize the bounding rect
    #     cv2.rectangle(cropped, (x, y), (x + w, y + h), 255, 1)

    # #cv2.drawContours(cropped_thresh, cropped_contours, -1, (255, 255, 0), 1)

    # cv2.imshow("output",cropped_thresh)
    # cv2.waitKey()
    #cv2_imshow(cropped)
    #cv2_imshow(cv2.drawContours(img, [sorted[-2]], -1, (0,255,0), 3))
    # contours, hierarchy = cv2.findContours(cropped_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #cv2_imshow(cv2.drawContours(cropped, contours, -1, (0,255,0), 3))

    # edges = cv2.Canny(cropped_thresh,50,150,apertureSize = 3)
    
    # # This returns an array of r and theta values
    # lines = cv2.HoughLines(edges,1,np.pi/180, 200)
    
    # # The below for loop runs till r and theta values 
    # # are in the range of the 2d array
    # possible = []
    # maxX = 0
    # for line in lines:
    #   for r,theta in line:
            
    #       # Stores the value of cos(theta) in a
    #       a = np.cos(theta)
        
    #       # Stores the value of sin(theta) in b
    #       b = np.sin(theta)
            
    #       # x0 stores the value rcos(theta)
    #       x0 = a*r
            
    #       # y0 stores the value rsin(theta)
    #       y0 = b*r
            
    #       # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
    #       x1 = int(x0 + 1000*(-b))
            
    #       # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
    #       y1 = int(y0 + 1000*(a))
        
    #       # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
    #       x2 = int(x0 - 1000*(-b))
            
    #       # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
    #       y2 = int(y0 - 1000*(a))

    #       if x1 > maxX and x1 < cropped.shape[1] / 4 and abs(x2-x1) < 10 and abs(y2-y1) > cropped.shape[0] * 0.8:
    #         #maxX = x1
    #         possible.append([x1, x2, y1, y2])
    #         cv2.line(cropped,(x1, y1), (x2, y2), (0,0,255),2)
            
            
    #       # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
    #       # (0,0,255) denotes the colour of the line to be 
    #       #drawn. In this case, it is red. 


    # maxLine = possible[0]
    # for i in possible:
    #   if i[0] > maxLine[0]:
    #     maxLine = i

    # cv2.imshow("cropped1", cropped)
    # cv2.waitKey()
