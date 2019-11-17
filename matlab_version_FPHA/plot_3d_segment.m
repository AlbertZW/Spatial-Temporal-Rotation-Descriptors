function [] = plot_3d_segment(start_point, end_point, plotarg)
    if start_point(1) < end_point(1)
        X = start_point(1): 1e-4: end_point(1);
    else
        X = start_point(1): -1e-4: end_point(1);
    end
    step_length = abs((start_point(1) - end_point(1)) / 1e-4);
    
    Y_step = abs(start_point(2) - end_point(2)) / step_length;
    if start_point(2) < end_point(2)
        Y = start_point(2): Y_step: end_point(2);
    else
        Y = start_point(2): -Y_step: end_point(2);
    end
    
    Z_step = abs(start_point(3) - end_point(3)) / step_length;
    if start_point(3) < end_point(3)
        Z = start_point(3): Z_step: end_point(3);
    else
        Z = start_point(3): -Z_step: end_point(3);
    end
    
    plot3(X, Y, Z, plotarg);
    grid on;
    
%     plot3(start_point(1), start_point(2), start_point(3), '-xb');
%     plot3(end_point(1), end_point(2), end_point(3), '-xb')
end

