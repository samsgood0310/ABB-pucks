MODULE Module1
    VAR num WPW:=0;
    VAR num WRD:=0;
    VAR bool ready_flag:= FALSE;
    VAR bool image_processed:= FALSE;
    CONST num gripHeight:= 10;
    CONST num safeHeight:= 60; ! Previously 120
    PERS num offset{2};
    PERS num angle:= 0;
    VAR speeddata vSpeed:= v500;
    VAR num vektor{100};

    ! Lage arrays for posisjon og orientering av alle pucker samlet.
    ! Brukes i stackPucks
    PERS robtarget puck_positions{30};
    PERS num angles{30};
    PERS num numberOfPucks:= 30;
    
    VAR triggdata slipp;
    
    VAR robtarget puck_target;
    PERS num offset_x;
    PERS num offset_y;
    VAR robtarget rob1;
    PERS robtarget randomTarget;
    PERS num image_height:=0;
    
    VAR robtarget gripper_target;
    VAR robtarget get_puck_target;
    VAR robtarget put_puck_target;
    VAR num puck_angle;

    VAR bool finished:=FALSE;

    CONST robtarget middleOfTable:=[[0,0,0],[0,1,0,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget overview:=[[0,0,500],[0,1,0,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    PERS robtarget puck_position:=[[-72.1875,35.9722,0],[0,1,0,0],[-1,0,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];
    CONST robtarget testDist:=[[70,150,10],[0,1,0,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget overview_part1:=[[0,0,505],[0,0.707106781,-0.707106781,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];

    TASK PERS wobjdata wobjTableN:=[FALSE,TRUE,"",[[150,-500,8],[0.707106781,0,0,-0.707106781]],[[0,0,0],[1,0,0,0]]];
    PERS tooldata tGripper:=[TRUE,[[0,0,114.25],[0,0,0,1]],[1,[-0.095984607,0.082520613,38.69176324],[1,0,0,0],0,0,0]];
    
    CONST robtarget Target_60:=[[-86.867057946,441.301176976,912.5550923],[0.558791189,-0.251151105,-0.090047636,-0.785217774],[-1,-1,0,3],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_50:=[[-420.301104886,-35.661665053,930.419426084],[0.55737407,0.258337239,0.091522215,-0.783721699],[-1,-1,0,3],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];


    
    PROC main2()
        !closeGripper(TRUE);
        getPuckSmoothly Offs(middleOfTable, 150, 150, 0);
        putPuckSmoothly Offs(middleOfTable, 150, 150, 0), 60;
        WaitTime(5);
        MoveL Offs(middleOfTable, 0, 0, gripHeight), vSpeed,fine,tGripper\WObj:=wobjTableN;
        WaitTime(3);
        MoveL overview,vSpeed,fine,tGripper\WObj:=wobjTableN;
        !WaitTime(8);
        !MoveL Offs(overview_part1, 0, -200, 0), vSpeed,fine,tGripper\WObj:=wobjTableN;
        !WaitTime(8);
        !MoveL Offs(overview_part1, 0, -400, 0), vSpeed,fine,tGripper\WObj:=wobjTableN;
    ENDPROC
    
    PROC main()
        closeGripper(FALSE);
        MoveJ overview,vSpeed,fine,tGripper\WObj:=wobjTableN;
        !MoveL testDist,v1000,fine,tGripper\WObj:=wobjTableN;
        
        WHILE TRUE DO        
            
            IF WPW <> 0 THEN
                WRD:=WPW;
                WPW:=0;
            
                TEST WRD
                    CASE 1:
                    MoveL overview,vSpeed,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                                            
                    
                    CASE 2:
                    !puck_target1.rot := OrientZYX(puck_angle1, 0, 180);
                    !MoveL puck_position,v1000,fine,tGripper\WObj:=wobjTableN;
                    MoveL Offs(puck_target, -55, 0, safeHeight),vSpeed,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                        
                    
                    WHILE NOT image_processed DO
                    ENDWHILE
                    image_processed:=FALSE;
                        
                    rob1 := CRobT(\Tool:=tGripper \Wobj:=wobjTableN);
                    getPuckSmoothly Offs(rob1, offset_x+55, offset_y, -120);
                    
                    putPuckSmoothly randomTarget, puck_angle;
                    
                    ready_flag:=TRUE;
                    
                    CASE 3:
                    FOR i FROM 0 TO 1 DO
                        
                    
                    ready_flag:=TRUE;
                    
                    WHILE NOT image_processed DO
                    ENDWHILE
                    image_processed:=FALSE;
                    
                    MoveL Offs(puck_target, -55, 0, safeHeight),vSpeed,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    WHILE NOT image_processed DO
                    ENDWHILE
                    image_processed:=FALSE;
                    
                    getPuckSmoothly puck_target;
                    
                    putPuckSmoothly Offs(middleOfTable, 0, 0, i*30), puck_angle;
                    
                    ENDFOR

                    CASE 4:
                    
                    ready_flag:=TRUE;
                    
                    WHILE NOT image_processed DO
                    ENDWHILE
                    image_processed:=FALSE;
                    
                    MoveL Offs(puck_target, -55, 0, 200),vSpeed,fine,tGripper\WObj:=wobjTableN;
                    
                    ready_flag:=TRUE;
                    
                    CASE 5:

                    MoveL overview,vSpeed,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    WHILE NOT image_processed DO
                    ENDWHILE
                    image_processed:=FALSE;
                    
                    MoveL Offs(puck_target, -55, 0, safeHeight),vSpeed,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    WHILE NOT image_processed DO
                    ENDWHILE
                    image_processed:=FALSE;
                    
                    MoveL Offs(puck_target, -55, 0, 500),vSpeed,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    CASE 6:

                    MoveL overview,vSpeed,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    WHILE NOT image_processed DO
                    ENDWHILE
                    image_processed:=FALSE;
                    
                    MoveL Offs(puck_target, -55, 0, safeHeight),vSpeed,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    WHILE NOT image_processed DO
                    ENDWHILE
                    image_processed:=FALSE;
                    
                    !rob1 := CRobT(\Tool:=tGripper \Wobj:=wobjTableN);
                    
                    !getPuckSmoothly Offs(rob1, offset_x+50, offset_y, -120);
                    getPuckSmoothly puck_target;
                    
                    putPuckSmoothly randomTarget, puck_angle;
                    
                    
                    
                    CASE 100:
                    ! Move gripper somewhere
                    ready_flag:=TRUE;
                    
                    MoveL gripper_target,vSpeed,z20,tGripper\WObj:=wobjTableN;
                    
                    CASE 101:
                    ! Pick up a puck
                    
                    getPuckSmoothly puck_target;
                    
                    CASE 102:
                    ! Place a puck
                    
                    putPuckSmoothly put_puck_target, puck_angle;
                    
                    CASE 103:
                    ! Throw puck
                    MoveJ overview,vSpeed,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    WHILE NOT image_processed DO
                    ENDWHILE
                    image_processed:=FALSE;
                    
                    MoveL Offs(puck_target, -55, 0, safeHeight),vSpeed,fine,tGripper\WObj:=wobjTableN;
                    ready_flag:=TRUE;
                    
                    WHILE NOT image_processed DO
                    ENDWHILE
                    image_processed:=FALSE;
                    
                    !rob1 := CRobT(\Tool:=tGripper \Wobj:=wobjTableN);
                    
                    !getPuckSmoothly Offs(rob1, offset_x+50, offset_y, -120);
                    getPuckSmoothly puck_target;
                    
                    MoveJ Target_50,v500,z20,tGripper\WObj:=wobjTableN;
                    TriggIO slipp, 0.3 \Time \DOp:= PneumaticGripper, 0;
                    TriggJ Target_60,v500,slipp,fine,tGripper\WObj:=wobjTableN;


                    
                    
            
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
        
        !MoveJ Offs(puck_position, -100, 0, safeHeight),vSpeed,z50,tGripper\WObj:=wobjTableN; 
        !MoveL Offs(puck_position, -50, 0, safeHeight),vSpeed,z100,tGripper\WObj:=wobjTableN;
        MoveL Offs(puck_position, -55, 0, gripHeight),vSpeed,z50,tGripper\WObj:=wobjTableN;
	    MoveL Offs(puck_position, 0, 0, gripHeight),v200,fine,tGripper\WObj:=wobjTableN;
        closeGripper(TRUE);
	    !MoveL Offs(puck_position, 0, 0, gripHeight),v100,fine,tGripper\WObj:=wobjTableN;
        MoveJ Offs(puck_position, 0, 0, gripHeight + 10),vSpeed,fine,tGripper\WObj:=wobjTableN;
        
    ENDPROC
    
    ! Plassere puck
    PROC putPuckSmoothly(robtarget toTarget, num angle)
        
        toTarget.rot := OrientZYX(-angle, 0, 180);
        MoveJ Offs(toTarget, 0, 0, gripHeight + 10),vSpeed,z50,tGripper\WObj:=wobjTableN;
        !MoveJ Offs(toTarget, 0, 0, gripHeight+50),vSpeed,fine,tGripper\WObj:=wobjTableN;
        MoveL Offs(toTarget, 0, 0, gripHeight),v200,fine,tGripper\WObj:=wobjTableN;
        closeGripper(FALSE);        
	    MoveJ Offs(toTarget, 0, 0, safeHeight),vSpeed,z5,tGripper\WObj:=wobjTableN;
        
    ENDPROC
    
    PROC stackPucks()
        
        FOR puckNum FROM 1 TO numberOfPucks DO
            MoveJ Offs(puck_positions{puckNum}, 0, 0, safeHeight), vSpeed, z50, tGripper\WObj:=wobjTableN;
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
    
    PROC closeGripper(bool state)
        WaitTime 0.1;
        IF state=TRUE THEN
          setDO PneumaticGripper, 1;  
        ELSEIF state=FALSE THEN
          setDO PneumaticGripper, 0;  
        ENDIF
        WaitTime 0.2;
    ENDPROC
    
ENDMODULE
