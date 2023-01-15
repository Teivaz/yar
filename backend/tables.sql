CREATE TYPE part_of_speech AS ENUM ('proper', 'noun', 'verb', 'adjective', 'pronoun', 'numeral', 'adverb', 'transgressive', 'participle', 'auxiliary');

CREATE TABLE lemmas (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    text text NOT NULL,
    part_of_speech part_of_speech NOT NULL,
    grammemes jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE word_forms (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    lemma_id integer NOT NULL REFERENCES lemmas(id) ON DELETE CASCADE ON UPDATE CASCADE,
    text text NOT NULL,
    grammemes jsonb NOT NULL DEFAULT '{}'::jsonb
);
