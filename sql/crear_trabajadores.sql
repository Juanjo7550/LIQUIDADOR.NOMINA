CREATE TABLE Empleado(
    codigo_empleado VARCHAR(10) PRIMARY KEY NOT NULL,
    nombre VARCHAR(20) NOT NULL,
    salario_base DECIMAL(15,2) NOT NULL, 
    dias_trabajados INT NOT NULL,
    horas_extra_diurnas DECIMAL(10,2) DEFAULT 0 , 
    horas_extra_nocturnas DECIMAL(10,2) DEFAULT 0,
    horas_extra_dominicales_diurnas DECIMAL(10,2) DEFAULT 0, 
    horas_extra_dominicales_nocturnas DECIMAL(10,2) DEFAULT 0,
    horas_recargo_nocturno DECIMAL(10,2) DEFAULT 0, 
    horas_recargo_dominical_festivo DECIMAL(10,2) DEFAULT 0
)