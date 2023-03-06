### Deliverables

#### Available outcome variables
- [ ] Submission scores (assigned by REF)
- [ ] ICS scores (imputed)
- [ ] Underlying output impact score (tbd)

#### Main insight structure

##### Submission level
`outcome` by submission `characteristics`
- [ ] Using submission-level `characteristics`
- [ ] Using ICS-level `characteristics` aggregated to the submission level
- [ ] Using output-level `characteristics` aggregated to the submission level

##### ICS level
`outcome` by ICS level `characteristics`
- [ ] Using ICS-level `characteristics`
- [ ] Using output-level `characteristics` aggregated to the submission

##### Output level
`outcome` by output level `characteristics`
- [ ] Using output-level `characteristics`

#### Output types
1. Bar plots showing average `outcome` by `characteristics` of choice
2. Geographic maps showing (combinations of) `outcome` (and secondary characteristic)
3. Heat maps to show average `outcome` and two `characteristics`
4. Multivariate 'impact' plots indicating how a `characteristic` affects an `outcome` (e.g. coefficients, Shapley values etc.)

### General data wrangling to-do's

#### Submission level
- [x] Extract data at the submission level
- [ ] Extract `characteristics` for each submission
  - [ ] Department `characteristics`
  - [ ] Submission `characteristics`
  - [ ] University `characteristics`
  - [ ] Geographic `characteristics`
  - [ ] ...

#### ICS level
- [x] Extract data at the ICS level
  - [ ] Text fields
  - [ ] Static `characteristics`
  - [ ] Underlying output identifiers
  - [ ] ...
- [ ] Extract `characteristics` for each individual ICS
  - [ ] Textual `characteristics`
    - [ ] Model topics
    - [ ] Model writing style
    - [ ] ...
- [ ] Extract `outcome` variable (score / value)
  - [ ] Model ICS' level scores through departmental level scores
  - [ ] ...

#### Underlying output level
- [ ] Extract data at the underlying output level
  - [ ] Altmetric
  - [ ] Author characteristics
  - [ ] Author affiliations
  - [ ] Journal characteristics
  - [ ] Abstract of text
  - [ ] Keywords
  - [ ] Citations
  - [ ] ...
- [ ] Extract `characteristics` for each underlying output
  - [ ] ...