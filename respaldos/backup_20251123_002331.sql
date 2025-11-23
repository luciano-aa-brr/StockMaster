--
-- PostgreSQL database dump
--

\restrict PTCq995KVVz3ey32LPfeod9GzTkKIlXuUaZm0HeboGvyhl5BQOuOumKZ1Ynpv54

-- Dumped from database version 13.23 (Debian 13.23-1.pgdg13+1)
-- Dumped by pg_dump version 13.23 (Debian 13.23-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: productos; Type: TABLE; Schema: public; Owner: usuario
--

CREATE TABLE public.productos (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    precio numeric(10,2) NOT NULL,
    stock integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.productos OWNER TO usuario;

--
-- Name: productos_id_seq; Type: SEQUENCE; Schema: public; Owner: usuario
--

CREATE SEQUENCE public.productos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.productos_id_seq OWNER TO usuario;

--
-- Name: productos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: usuario
--

ALTER SEQUENCE public.productos_id_seq OWNED BY public.productos.id;


--
-- Name: productos id; Type: DEFAULT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.productos ALTER COLUMN id SET DEFAULT nextval('public.productos_id_seq'::regclass);


--
-- Data for Name: productos; Type: TABLE DATA; Schema: public; Owner: usuario
--

COPY public.productos (id, nombre, descripcion, precio, stock) FROM stdin;
1	Cargador USB-C	Cargador carga rapida 20W	7000.00	50
2	Auriculares Bluetooth	Cancelacion de ruido	25000.00	30
3	Smartwatch Deportivo	Monitor cardiaco y GPS	45000.00	20
4	Parlante Bluetooth	Parlante resistente al agua	200000.00	20
\.


--
-- Name: productos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario
--

SELECT pg_catalog.setval('public.productos_id_seq', 4, true);


--
-- Name: productos productos_pkey; Type: CONSTRAINT; Schema: public; Owner: usuario
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict PTCq995KVVz3ey32LPfeod9GzTkKIlXuUaZm0HeboGvyhl5BQOuOumKZ1Ynpv54

