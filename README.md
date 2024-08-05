# CAI Utils

This repository contains a selection of useful functions, scripts, and notebooks for building CAI bots with GCP.


## Repository Structure

The repo is structured as follows:

```
.
├── archive/
├── templates/
├── notebooks/
│   ├── notebook_1_name/
│   │   └── notebook_1_name.ipynb
│   ├── notebook_2_name/
│   │   └── ...
│   └── ...
├── cloud_functions/
│   ├── function_1_name/
│   │   ├── README.md
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   ├── tests/
│   │   │   ├── test_function_1_name.py
│   │   │   └── ...
│   │   └── ...
│   ├── function_2_name/
│   │   └── ...
│   └── ...
└── ...
```

## Contributing

When contributing, please create a descriptively named feature branch (e.g., `{last-name}/{functionality}`) to use for development and then a pull request to bring your additions into `main` when they're ready.

### Adding a Cloud Function

To add a cloud function, please refer to the template directory in `/templates/cloud_function`. New functions should have a detailed README that includes documentation of the functionality, problems solved, instructions, and any limitations a user should be aware of. The function directory should also include unit tests to cover basic functionality.