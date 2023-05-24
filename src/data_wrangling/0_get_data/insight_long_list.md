### Deliverables

#### Available outcome variables
- [+] Submission scores (assigned by REF)
- [-] ICS scores (imputed)
- [-] Underlying output impact score (tbd)

#### Main insight structure

##### Submission level
`outcome` by submission `characteristics`
- [+] Using submission-level `characteristics`
- [+] Using ICS-level `characteristics` aggregated to the submission level
- [-] Using output-level `characteristics` aggregated to the submission level

Dataset: 1-2K x K

##### ICS level
`outcome` by ICS level `characteristics`
- [-] Using ICS-level `characteristics`
- [-] Using output-level `characteristics` aggregated to the submission

Dataset: 6.5K x K

##### Output level
`outcome` by output level `characteristics`
- [-] Using output-level `characteristics`

Dataset 30K x K

#### Output types
1. Bar plots showing average `outcome` by `characteristics` of choice (`fun_bar`)
2. Geographic maps showing (combinations of) `outcome` (and secondary characteristic)
3. Descriptive plot of the various topics that are present in a subset (unigram and bigrams)
5. Heat maps to show average `outcome` and two `characteristics`
6. Multivariate 'impact' plots indicating how a `characteristic` affects an `outcome` (e.g. coefficients, Shapley values etc.)

### General data wrangling to-do's

#### Submission level
- [x] Extract data at the submission level
- [ ] Extract `characteristics` for each submission
  - [ ] Department `characteristics`
    - [ ] Number of FTE (numeric)
    - [ ] Number of graduates (numeric)
  - [ ] Submission `characteristics`
  - [ ] University `characteristics`
  - [ ] Geographic `characteristics`
  - [ ] Environment `characteristics`
  - [ ] ...

#### ICS level
- [x] Extract data at the ICS level
  - [x] Text fields
  - [x] Static `characteristics`
  - [x] Underlying output identifiers
- [+] Extract `characteristics` for each individual ICS
  - [+] Textual `characteristics`
    - [+] Model topics (`K`-vector with proportions)
    - [+] Model writing style / patterns (numeric)
    - [ ] Model sentiment
    - [ ] Counting
    - [ ] ...
- [-] Extract `outcome` variable (score / value)
  - [-] Model ICS' level scores through departmental level scores
  - [-] ...

#### Underlying output level
- [-] Extract data at the underlying output level
  - [ ] Altmetric
  - [-] Author characteristics
  - [-] Author affiliations
  - [-] Journal characteristics
  - [-] Abstract of text
  - [-] Keywords
  - [-] Citations
  - [-] ...
- [-] Extract `characteristics` for each underlying output
  - [-] ...