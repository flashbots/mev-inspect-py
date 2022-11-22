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
-- Name: swaps; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.swaps (
    created_at timestamp without time zone DEFAULT now(),
    abi_name character varying(1024) NOT NULL,
    transaction_hash character varying(66) NOT NULL,
    block_number numeric NOT NULL,
    protocol character varying(256),
    contract_address character varying(256) NOT NULL,
    from_address character varying(256) NOT NULL,
    to_address character varying(256) NOT NULL,
    token_in_address character varying(256) NOT NULL,
    token_in_amount numeric NOT NULL,
    token_out_address character varying(256) NOT NULL,
    token_out_amount numeric NOT NULL,
    trace_address integer[] NOT NULL,
    error character varying(256),
    transaction_position numeric
);


ALTER TABLE public.swaps OWNER TO postgres;

--
-- Name: swaps swaps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.swaps
    ADD CONSTRAINT swaps_pkey PRIMARY KEY (block_number, transaction_hash, trace_address);


--
-- PostgreSQL database dump complete
--

