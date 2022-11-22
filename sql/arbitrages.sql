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
-- Name: arbitrages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.arbitrages (
    id character varying(256) NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    account_address character varying(256) NOT NULL,
    profit_token_address character varying(256) NOT NULL,
    block_number numeric NOT NULL,
    transaction_hash character varying(256) NOT NULL,
    start_amount numeric NOT NULL,
    end_amount numeric NOT NULL,
    profit_amount numeric NOT NULL,
    error character varying(256),
    protocols character varying(256)[] DEFAULT '{}'::character varying[]
);


ALTER TABLE public.arbitrages OWNER TO postgres;

--
-- Name: arbitrages arbitrages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arbitrages
    ADD CONSTRAINT arbitrages_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

