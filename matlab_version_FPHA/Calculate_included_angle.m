function included_angle = Calculate_included_angle(vec1, vec2)
%CALCULATE_INCLUDED_ANGLE

dotProd = vec1 * vec2';
normProd = (vec1 * vec1') * (vec2 * vec2');
cosined_angle = dotProd / normProd;
included_angle = acos(cosined_angle);

end

