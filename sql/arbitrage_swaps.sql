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
-- Name: arbitrage_swaps; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.arbitrage_swaps (
    created_at timestamp without time zone DEFAULT now(),
    arbitrage_id character varying(1024) NOT NULL,
    swap_transaction_hash character varying(66) NOT NULL,
    swap_trace_address integer[] NOT NULL
);


ALTER TABLE public.arbitrage_swaps OWNER TO postgres;

--
-- Name: arbitrage_swaps arbitrage_swaps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arbitrage_swaps
    ADD CONSTRAINT arbitrage_swaps_pkey PRIMARY KEY (arbitrage_id, swap_transaction_hash, swap_trace_address);


--
-- Name: arbitrage_swaps_swaps_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX arbitrage_swaps_swaps_idx ON public.arbitrage_swaps USING btree (swap_transaction_hash, swap_trace_address);


--
-- Name: arbitrage_swaps arbitrage_swaps_arbitrage_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.arbitrage_swaps
    ADD CONSTRAINT arbitrage_swaps_arbitrage_id_fkey FOREIGN KEY (arbitrage_id) REFERENCES public.arbitrages(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

