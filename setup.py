from distutils.core import setup
from setuptools import find_packages
with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()
    setup(name='nonebot_plugin_pvz',  # 包名
          version='1.0.2',  # 版本号
          description='A plugin of nonebot2, which is support service to play pvz in group chat.',
          long_description=long_description,
          author='longchengguxiao',
          author_email='1298919732@qq.com',
          url='http://www.lcgx.space/home',
          install_requires=[
              "numpy",
              "pillow",
              "nonebot2>=2.0.0a16",
              "nonebot-adapter-onebot>=2.0.0b1"
          ],
          license='MIT License',
          packages=find_packages(),
          platforms=["all"],
          classifiers=['Intended Audience :: Developers',
                       'Operating System :: OS Independent',
                       'Natural Language :: Chinese (Simplified)',
                       'Programming Language :: Python',
                       'Programming Language :: Python :: 3.8',
                       'Programming Language :: Python :: 3.9',
                       'Topic :: Software Development :: Libraries'
                       ],
          )
