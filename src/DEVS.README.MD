### Testing locally
`python setup.py develop`

### Deploying package
`python setup.py sdist bdist_wheel`
`twine upload --skip-existing dist/*`