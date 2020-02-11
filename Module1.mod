MODULE Module1
    PERS num WPW:=0;
    PERS num WRD:=2;
    PERS bool ready_flag:= FALSE;
    PERS bool image_processed:= FALSE;
    CONST num gripHeight:= 10;
    CONST num safeHeight:= 120;
    PERS num offset{2};
    PERS num angle:= 0;

    ! Lage arrays for posisjon og orientering av alle pucker samlet.
    ! Brukes i stackPucks
    PERS robtarget puck_positions{30};
    PERS num angles{30};
    PERS num numberOfPucks:= 30;
    
    PERS robtarget puck_target1;
    PERS num puck_angle1;
    PERS num offset_x;
    PERS num offset_y;
    VAR robtarget rob1;
    PERS robtarget randomTarget;
    
	CONST robtarget middleOfTable:=[[0,0,safeHeight],[0,1,0,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    ! CONST robtarget middleOfTable:=[[0,0,safeHeight],[0,1,0,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget overview:=[[0,0,400],[0,1,0,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    PERS robtarget puck_position:=[[-72.1875,35.9722,0],[0,1,0,0],[-1,0,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];
    CONST robtarget testDist:=[[70,150,10],[0,1,0,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];

    TASK PERS wobjdata wobjTableN:=[FALSE,TRUE,"",[[150,-500,8],[0.707106781,0,0,-0.707106781]],[[0,0,0],[1,0,0,0]]];

    
    PROC main2()
        WHILE TRUE DO
            waitForPython;
            MoveL rob1,v200,z10,tGripper\WObj:=wobjTableN;
            ready_flag:=TRUE;
        ENDWHILE
    ENDPROC
    
    PROC main()
        closeGripper(FALSE);
        MoveL overview,v1000,fine,tGripper\WObj:=wobjTableN;
        !MoveL testDist,v1000,fine,tGripper\WObj:=wobjTableN;
        
        WHILE TRUE DO        
            
            WaitTime(1);
            IF WPW <> 0 THEN
                WRD:=WPW;
            
                TEST WPW
                    CASE 1:
                    WPW:= 0;
                    MoveL Offs(overview,-50, 0,0),v1000,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    CASE 2:
                    WPW:= 0;
		    
                    MoveL Offs(puck_target1, -50, 0, safeHeight),v1000,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    waitForPython;
                    
                    rob1 := CRobT(\Tool:=tGripper \Wobj:=wobjTableN);
                    getPuckSmoothly Offs(rob1, offset_x+50, offset_y, -120);
                    
                    putPuckSmoothly randomTarget, puck_angle1;
                    
                    ready_flag:=TRUE;
                    
                    CASE 3:
                    WPW:= 0;
					
					MoveL Offs(puck_target1, -50, 0, safeHeight),v1000,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    waitForPython;
                    
                    rob1 := CRobT(\Tool:=tGripper \Wobj:=wobjTableN);
                    getPuckSmoothly Offs(rob1, offset_x+50, offset_y, -120);
                    
                    putPuckSmoothly middleOfTable, puck_angle1;
					
					MoveL Offs(puck_target2, -50, 0, safeHeight),v1000,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    waitForPython;
                    
                    rob1 := CRobT(\Tool:=tGripper \Wobj:=wobjTableN);
                    getPuckSmoothly Offs(rob1, offset_x+50, offset_y, -120);
                    
                    putPuckSmoothly Offs(middleOfTable, 0, 0, 30), puck_angle2;
                    
                    CASE 4:
                    
            
                ENDTEST
            ENDIF
            WRD:=0;
            
            
        ENDWHILE 
        
    ENDPROC
    
    PROC waitForPython()
    	WHILE NOT image_processed DO
        ENDWHILE
    	image_processed:=FALSE;
    ENDPROC 
       
    ! Flytte valgt puck til midten
    PROC movePuckToMiddle(robtarget fromTarget)
        
        getPuckSmoothly fromTarget;
        putPuckSmoothly middleOfTable, angle;
        
    ENDPROC
    
    
    ! Plukke opp puck
    PROC getPuckSmoothly (robtarget puck_position)
        
        MoveJ Offs(puck_position, -100, 0, safeHeight),v500,z50,tGripper\WObj:=wobjTableN;
        MoveL Offs(puck_position, -100, 0, gripHeight),v200,z50,tGripper\WObj:=wobjTableN;
	    MoveL Offs(puck_position, 0, 0, gripHeight),v100,fine,tGripper\WObj:=wobjTableN;
        closeGripper(TRUE);
	    !MoveL Offs(puck_position, 0, 0, gripHeight),v100,fine,tGripper\WObj:=wobjTableN;
        MoveJ Offs(puck_position, 0, 0, gripHeight+50),v200,fine,tGripper\WObj:=wobjTableN;
        
    ENDPROC
    
    ! Plassere puck
    PROC putPuckSmoothly(robtarget toTarget, num angle)
        
        MoveJ Offs(toTarget, 0, 0, safeHeight),v500,z50,tGripper\WObj:=wobjTableN;
        toTarget.rot := OrientZYX(angle, 0, 180);
        MoveJ Offs(toTarget, 0, 0, gripHeight+50),v500,fine,tGripper\WObj:=wobjTableN;
        MoveJ Offs(toTarget, 0, 0, gripHeight),v100,fine,tGripper\WObj:=wobjTableN;
        closeGripper(FALSE);        
	    MoveJ Offs(toTarget, 0, 0, safeHeight),v500,fine,tGripper\WObj:=wobjTableN;
        
    ENDPROC
    
    PROC stackPucks()
        
        FOR puckNum FROM 1 TO numberOfPucks DO
            MoveJ Offs(puck_positions{puckNum}, 0, 0, safeHeight), v500, z50, tGripper\WObj:=wobjTableN;
            ready_flag:=TRUE;
            !WHILE NOT image_processed DO ! vent på Python
            !ENDWHILE
            !image_processed:= FALSE;
            getPuckSmoothly puck_positions{puckNum};
            putPuckSmoothly Offs(middleOfTable, 0, 0, 30*(puckNum-1)), angles{puckNum};
            
        ENDFOR
        ! Flytt over puck og sett ready_flag:=1; Ta bilde og fortsett:
        ! movePuckToMiddle puck_position;    
    ENDPROC
    
ENDMODULE
