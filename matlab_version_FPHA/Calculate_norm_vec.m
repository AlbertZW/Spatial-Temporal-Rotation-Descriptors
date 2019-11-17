function norm_vec = Calculate_norm_vec(vec1, vec2)
%CALCULATE_NORM_VEC

unnormed_norm = cross(vec1, vec2);
norm = sqrt(unnormed_norm * unnormed_norm');
norm_vec = unnormed_norm / norm;

end

