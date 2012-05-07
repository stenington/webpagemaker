BEGIN;
ALTER TABLE `api_page`
    ADD `original_url` varchar(200) NOT NULL;
COMMIT;
