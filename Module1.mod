MODULE Module1
    PERS num WPW:=0;
    PERS num WRD:=0;
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
    
    PERS robtarget puck_target;
    PERS num puck_angle;
    PERS num offset_x;
    PERS num offset_y;
    VAR robtarget rob1;
    PERS robtarget randomTarget;
    

    CONST robtarget middleOfTable:=[[0,0,safeHeight],[0,1,0,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget overview:=[[0,0,400],[0,1,0,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    PERS robtarget puck_position:=[[-72.1875,35.9722,0],[0,1,0,0],[-1,0,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];
    CONST robtarget testDist:=[[70,150,10],[0,1,0,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];

    TASK PERS wobjdata wobjTableN:=[FALSE,TRUE,"",[[150,-500,8],[0.707106781,0,0,-0.707106781]],[[0,0,0],[1,0,0,0]]];

    
    PROC main2()
        WHILE TRUE DO
            WHILE NOT image_processed DO
            ENDWHILE
            image_processed:=FALSE;
            MoveL rob1,v200,z10,tGripper\WObj:=wobjTableN;
            ready_flag:=TRUE;
        ENDWHILE
    ENDPROC
    
    PROC main()
        closeGripper(FALSE);
        MoveL middleOfTable,v1000,fine,tGripper\WObj:=wobjTableN;
        !MoveL testDist,v1000,fine,tGripper\WObj:=wobjTableN;
        
        WHILE TRUE DO        
            
            WaitTime(1);
            IF WPW <> 0 THEN
                WRD:=WPW;
            
                TEST WPW
                    CASE 1:
                    WPW:= 0;
                    MoveL Offs(overview,0,0,0),v1000,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    CASE 2:
                    WPW:= 0;
                    !puck_target1.rot := OrientZYX(puck_angle1, 0, 180);
                    !MoveL puck_position,v1000,fine,tGripper\WObj:=wobjTableN;
                    MoveL Offs(puck_target, -50, 0, safeHeight),v1000,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    WHILE NOT image_processed DO
                    ENDWHILE
                    image_processed:=FALSE;
                    
                    rob1 := CRobT(\Tool:=tGripper \Wobj:=wobjTableN);
                    getPuckSmoothly Offs(rob1, offset_x+50, offset_y, -120);
                    
                    putPuckSmoothly randomTarget, puck_angle;
                    
                    ready_flag:=TRUE;
                    
                    CASE 3:
                    WPW:= 0;
                    stackPucks;
                    

                    CASE 4:
                    
            
                ENDTEST
            ENDIF
            WRD:=0;
            
            
        ENDWHILE 
        
    ENDPROC
       
    ! Flytte valgt puck til midten
    PROC movePuckToMiddle(robtarget fromTarget)
        
        getPuckSmoothly fromTarget;
        putPuckSmoothly middleOfTable, angle;
        
    ENDPROC
    
    
    ! Plukke opp puck
    PROC getPuckSmoothly (robtarget puck_position)
        
        !MoveJ Offs(puck_position, -100, 0, safeHeight),v500,z50,tGripper\WObj:=wobjTableN; ! safe_height er allerede satt i Python som 120
        MoveJ Offs(puck_position, -50, 0, safeHeight),v500,z0,tGripper\WObj:=wobjTableN;
        MoveJ Offs(puck_position, -50, 0, gripHeight),v500,z0,tGripper\WObj:=wobjTableN;
	    MoveL Offs(puck_position, 0, 0, gripHeight),v100,fine,tGripper\WObj:=wobjTableN;
        closeGripper(TRUE);
	    !MoveL Offs(puck_position, 0, 0, gripHeight),v100,fine,tGripper\WObj:=wobjTableN;
        MoveJ Offs(puck_position, 0, 0, gripHeight + 10),v500,fine,tGripper\WObj:=wobjTableN;
        
    ENDPROC
    
    ! Plassere puck
    PROC putPuckSmoothly(robtarget toTarget, num angle)
        
        toTarget.rot := OrientZYX(-angle, 0, 180);
        MoveJ Offs(toTarget, 0, 0, gripHeight + 10),v500,z50,tGripper\WObj:=wobjTableN;
        !MoveJ Offs(toTarget, 0, 0, gripHeight+50),v500,fine,tGripper\WObj:=wobjTableN;
        MoveL Offs(toTarget, 0, 0, gripHeight),v100,fine,tGripper\WObj:=wobjTableN;
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
