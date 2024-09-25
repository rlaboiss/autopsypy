# CHANGELOG

## 0.2.1 – 2024-09-24

- Put the package in an individual directory and use `__init__.py` This is more appropriate for standalone installations of PsychoPy, when setting the library path via preferences/general.

## 0.2.0 – 2024-09-24

- Adjust code for recent versions of PsychoPy. The module has been tested against PsychoPy versions 2023.1.2, 2024.1.4, and 2024.2.1. It may work with other versions.

## 0.1.3 – 2024-03-12

- Read entire CSV file when sniffing for delimiter bug fix)

## 0.1.2 – 2023-10-02

- Improve documentation
- Fix a bug that was resulting in wrong display of group sizes at the end of the session. The lines with value “no” in the “keep” columns were not being excluded.

## 0.1.1 – 2023-09-30

Add ChangeLog file and provide URL for it on the PyPI webpage

## 0.1.0 – 2023-09-30

Important changes in this release:

- A new argument desired_group_size is added to the class instantiation function AutoPsyPy(). This argument, whose value defaults to infinity (∞), has only informational value (i.e. does not affect the behavior of autopsyy) and is shown at the end of the experiment.
- Information on the number of participants in each group is shown at the end of the session.
- A new column entitled keep is added to the session CSV file. This column contains the value yes in the line corresponding to a successfully-run participant. Any other value appearing in this column indicates that the participant is excluded from the study.

This release add a backward-incompatibilty with version 0.0.6. Experiments started with version 0.0.6 or earlier should have their sessions.csv (or whatever name it has) file modified by adding a column keep filled with yes values.

## 0.0.6 – 2023-09-30

Improvements in documentation

## 0.0.5 – 2023-09-19

Fix link for the demo directory

## 0.0.4 – 2023-09-19

Add demo

## 0.0.3 – 2023-09-19

Fix documentation and ensure that condition column contains integers

## 0.0.2 – 2023-09-19

Fix documentation

## 0.0.1 – 2023-09-19

Initial release

<!---
Local Variables:
ispell-local-dictionary: "american"
eval: (auto-fill-mode -1)
eval: (visual-line-mode)
eval: (flyspell-mode)
End:
--->

<!--  LocalWords:  PsychoPy
 -->
