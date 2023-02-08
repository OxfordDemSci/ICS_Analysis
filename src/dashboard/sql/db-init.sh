psql -U $POSTGRES_USER -d $POSTGRES_DB -c \
"
CREATE ROLE reader LOGIN PASSWORD '${POSTGRES_RPASS}';

CREATE TABLE ics_2021(
  id INT PRIMARY KEY,
  institution_ukprn_code INT,
  institution_name VARCHAR(80),
  main_panel CHAR(1),
  unit_of_assessment_number SMALLINT,
  unit_of_assessment_name VARCHAR(80),
  multiple_submission_letter CHAR(1),
  multiple_submission_name VARCHAR(80),
  joint_submission VARCHAR(80),
  ref_impact_case_study_identifier CHAR(36),
  title VARCHAR(250),
  is_continued_from_2014 BOOLEAN,
  summary_impact_type VARCHAR(20),
  countries_iso3 CHAR(3)[] NOT NULL DEFAULT '{}',
  formal_partners VARCHAR(80)[] NOT NULL DEFAULT '{}',
  funding_programmes VARCHAR(250)[] NOT NULL DEFAULT '{}',
  global_research_identifiers VARCHAR(20)[] NOT NULL DEFAULT '{}',
  name_of_funders VARCHAR(80)[] NOT NULL DEFAULT '{}',
  researcher_orcids VARCHAR(19)[] NOT NULL DEFAULT '{}',
  grant_funding VARCHAR(80)[] NOT NULL DEFAULT '{}'
);
GRANT SELECT ON ics_2021 TO reader;

CREATE TABLE countries(
  iso3 INT PRIMARY KEY,
  country VARCHAR(30)
  UNIQUE (test_id)
);
GRANT SELECT ON mot TO reader;
"
