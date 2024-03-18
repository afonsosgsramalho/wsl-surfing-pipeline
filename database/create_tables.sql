CREATE TABLE "athletes" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "country" varchar,
  "name_country" varchar,
  "stance" varchar,
  "age" integer,
  "height" varchar,
  "weight" varchar,
  "hometown" varchar,
  "created_at" timestamp
);

CREATE TABLE "rankings" (
  "id" serial PRIMARY KEY,
  "ranking" integer,
  "athlete" varchar,
  "event" varchar,
  "score" integer,
  "created_at" timestamp
);

CREATE TABLE "cache_logs" (
  "link" varchar,
  "created_at" timestamp
);

ALTER TABLE "rankings" ADD FOREIGN KEY ("athlete") REFERENCES "athletes" ("name_country");
