<div align="center">
<sub>

Illustration by [Sean Sinclair](https://unsplash.com/@seanwsinclair) on Unplash.

</sub>

<br />

<img
  src="https://github.com/AWeirdScratcher/getllms/assets/90096971/3280e416-2e9a-4ae5-965d-c1c69d351d90"
  alt="Unplash / Sean Sinclair"
  />

# getllms - 0.5

The LLMs index. Uses the [LMStudio Catalog](https://github.com/lmstudio-ai/model-catalog).

`$ pip install getllms`

</div>

<br />

<details>
  <summary>
    <table>
      <thead>
        <tr>
          <th>In This Version</th>
        </tr>
      </thead>
    </table>
  </summary>
  <p>

**What's New**

- `0.5`: Support for Notebooks
- `0.4`: Minor fixes

  </p>
</details>

## List All LLMs.

List all LLMs available for use. Selected for you.

```python
import getllms

models = getllms.list_models()
```

<details>
    <summary>Output</summary>
<p>

```python
[
    Model(
        name='Samantha 1.1 7B',
        description='Samantha has been trained in philos…',
        files=[ …(2) ]
    ),
    Model(
        name='Redmond-Puffin-13B-V1.3',
        description='Redmond-Puffin-13B is one of the wo…',
        files=[ …(1) ]
    )
]
```

</p>
</details>

<br />

## See Trained LLMs.

Get the trained ones for a specific model. Select the one that meets your system requirements.

```python
models[0].files # trained samantha 1.1 7b
```

<details>
    <summary>Output & More</summary>
<p>

**Output**

```python
FileCollection(
    best=ModelFile(
        name='samantha-1.1-llama-7b.ggmlv3.q6_K.bin',
        size=5528904320,
        url='https://huggingface.co/TheBlok…'
    ),
    +1
)
```

***

**More**

Additionally, you can see all the available model files:

```python
models[0].files.all # [ ModelFile(name='samantha-1.1-llama-…'), … ]
```

</p>
</details>

<br />

## Download LLMs.

Download the LLM that's right for you.

```python
best = models[0].files.best
best.download()
```

<details>
    <summary>Output</summary>
<p>

```python
Downloading... 116.44MB / 5.15GB (2.00%)
```

</p>
</details>

***

<div align="center">

<sub>

Illustration by [Milad Fakurian](https://unsplash.com/@fakurian) on Unplash.

</sub>

<br />

<img src="https://github.com/AWeirdScratcher/getllms/assets/90096971/42c9b72e-cd0c-4a88-85f9-dc0dd06ae7a2" />

# More

User guides, and many more.

Learn how to master `getllms` in under five minutes.

</div>

<br />

<details>
  <summary>
    <table>
      <thead>
        <tr>
          <th>Table of Contents</th>
        </tr>
      </thead>
    </table>
  </summary>
  <p>

**TOC**

1. [Updating the Catalog](#updating-the-catalog)
2. [Dataclasses](#dataclasses)
   - [`Model`](#model)
   - [`ModelFileCollection`](#modelfilecollection)
     - `find()`
   - [`ModelFile`](#modelfile)
     - `download()`
    
  </p>
</details>

## Updating the Catalog

When `getllms` is downloaded, the index file is automatically installed inside of `getllms.data` and is already compressed.

You can get the latest version of the model catalogue using:

```python
from getllms import download_model_data, erase_data

erase_data(reload=True) # erase the previous version
download_model_data() # download the latest ones

# now list all the models.
```

## Dataclasses

Below is a list of attributes of the dataclasses (from `getllms.model`).

### Model

Represents the info of an LLM model.

```python
class Model:
    name: str
    date_published: str
    description: str
    author: dict[str, str]
    n_params: str # (e.g., 7B)
    canonical_url: str
    download_url: str # note: NOT the raw file
    trained_for: Literal['chat', 'instruct', 'other']
    files: ModelFileCollection
```

### ModelFileCollection

A set of model files.

```python
class ModelFileCollection:
    all: List[ModelFile]
    most_capable: ModelFile
    best: ModelFile # (alias: most_capable)
    economical: ModelFile
```

#### find()

Find a model file by name.

Args:
- name (`str`): The name.

```python
def find(self, name: str) -> ModelFile
```

### ModelFile

A model file.

```python
class ModelFile:
    name: str
    url: str
    size: int
    quantization: str
    format: Literal['ggml', 'gguf']
    publisher: dict[str, str]
```

#### download()

Download the model.

Args:
- to (`str`, optional): The file destination.

```python
def download(self, *, to: Optional[str] = None)
```

***

<div align="center">

© 2023 AWeirdDev, Catalog by [LMStudio](https://github.com/lmstudio-ai)

</div>
