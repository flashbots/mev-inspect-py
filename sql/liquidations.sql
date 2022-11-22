--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4
-- Dumped by pg_dump version 15.0 (Ubuntu 15.0-1.pgdg22.04+1)

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
-- Name: liquidations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.liquidations (
    created_at timestamp without time zone DEFAULT now(),
    liquidated_user character varying(256) NOT NULL,
    liquidator_user character varying(256) NOT NULL,
    debt_token_address character varying(256) NOT NULL,
    debt_purchase_amount numeric NOT NULL,
    received_amount numeric NOT NULL,
    protocol character varying(256),
    transaction_hash character varying(66) NOT NULL,
    trace_address character varying(256) NOT NULL,
    block_number numeric NOT NULL,
    received_token_address character varying(256),
    error character varying(256)
);


ALTER TABLE public.liquidations OWNER TO postgres;

--
-- Name: liquidations liquidations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.liquidations
    ADD CONSTRAINT liquidations_pkey PRIMARY KEY (transaction_hash, trace_address);


--
-- PostgreSQL database dump complete
--

