SELECT codigo_empleado, 
    nombre, salario_base, 
    dias_trabajados, 
    horas_extra_diurnas, 
    horas_extra_nocturnas, 
    horas_extra_dominicales_diurnas, 
    horas_extra_dominicales_nocturnas, 
    horas_recargo_nocturno, 
    horas_recargo_dominical_festivo
FROM public.Empleado
LIMIT 1000;


DELETE FROM empleado