CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0
);

INSERT INTO productos (nombre, descripcion, precio, stock) VALUES
('Cargador USB-C', 'Cargador carga rapida 20W', 7000.00, 50),
('Auriculares Bluetooth', 'Cancelacion de ruido', 25000.00, 30),
('Smartwatch Deportivo', 'Monitor cardiaco y GPS', 45000.00, 20);