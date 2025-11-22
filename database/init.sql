CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0
);

--datos de prueba <3 

INSERT INTO productos (nombre. descripcion, precio, stock) VALUES
('Cargador USB-C', 'Cargador rapido de 20w', 7.000, 50),
('Auriculares Inalambricos', 'Auriculares con cancelacion de ruido', 25.000, 30),
('Smartwatch Deportivo', 'Reloj inteligente con monitor de ritmo cardiaco', 45.000, 20);

