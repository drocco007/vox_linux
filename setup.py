from distutils.core import setup
setup(
    name='vox',
    version='0.1',
    packages=['vox'],
    entry_points="""
        [console_scripts]
        vox = vox.main
    """
    )
