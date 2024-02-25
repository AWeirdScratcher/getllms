from __future__ import annotations

from typing import Dict, List, Literal, Optional

from .download import download as DOWNLOAD


class Model:
    """Represents the info of an LLM model."""
    __slots__ = ("d",)
    d: dict
    
    def __init__(self, d: dict):
        self.d = d

    @property
    def name(self) -> str:
        """The name of the model."""
        return self.d['name']

    @property
    def date_published(self) -> str:
        """The publish date."""
        return self.d['datePublished']

    @property
    def description(self) -> str:
        """Model description."""
        return self.d['description']

    @property
    def author(self) -> dict:
        """Author data.

        Includes keys:
        - name: str
        - url: str
        - blurb: str
        """
        return self.d['author']

    @property
    def n_params(self) -> str:
        """The number of parameters the model has.

        Ex. 7B, 13B, ...
        """
        return self.d['numParameters']

    @property
    def canonical_url(self) -> str:
        """The canonical URL.

        Usually a Huggingface model page.
        """
        return self.d['resources']['canonicalUrl']

    @property
    def download_url(self) -> str:
        """The download URL.

        Usually a Huggingace model page.

        .. note ::

            This is not the raw file download URL.
        """
        return self.d['resources']['downloadUrl']

    @property
    def trained_for(self) -> Literal['chat', 'instruct', 'other']:
        """What the model was trained for.

        Could be:
        - chat: General chatting.
        - instruct: Instruct.
        - other: Other purposes.
        """
        return self.d['trainedFor']

    @property
    def files(self) -> ModelFileCollection:
        """Model files.
        
        Usually the trained ones.
        """
        models = {
            data['name']: ModelFile(data)
            for data in self.d['files']['all']
        }
        economic = self.d['files']['highlighted']['economical']
        most_cap = self.d['files']['highlighted'].get(
            'most_capable',
            economic
        )

        return ModelFileCollection(
            models,
            most_cap['name'],
            economic['name']
        )
    
    def download(
        self, 
        to: Optional[str] = None, 
        *, 
        type: Literal["economical", "best"] = "economical"
    ) -> None:
        """Download the model.
        
        Args:
            to (str, optional): Save file path.
            type (Literal["economical", "best"]): Model type.
        """
        self.files.download(to=to, type=type)
        

    def __repr__(self):
        return (
            f"Model(name={self.name!r}, "
            f"description='{self.description[:35]}…', "
            f"files=[ …({len(self.files)}) ])"
        )
        

class ModelFileCollection:
    """A set of model files."""
    __slots__ = (
        "m", 
        "_most_cap", 
        "_economic"
    )
    m: Dict[str, ModelFile]
    _most_cap: ModelFile
    _economic: ModelFile

    def __init__(
        self, 
        models: Dict[str, ModelFile], 
        most_cap: str, 
        economic: str
    ):
        self.m = models
        self._most_cap = models[most_cap]
        self._economic = models[economic]

    @property
    def all(self) -> List[ModelFile]:
        """All the models available for use."""
        return list(self.m.values())

    @property
    def most_capable(self) -> ModelFile:
        """The most capable model."""
        return self._most_cap

    @property
    def best(self) -> ModelFile:
        """The most capable model.

        (alias: ``most_capable``)
        """
        return self._most_cap

    @property
    def economical(self) -> ModelFile:
        """Model that matches the minimum system requirements.

        Just like the "economic seat" in planes.
        """
        return self._economic
    
    @property
    def economic(self) -> ModelFile:
        """Model that matches the minimum system requirements.

        Just like the "economic seat" in planes.
        """
        return self._economic
    

    def find(self, name: str) -> ModelFile:
        """Find a model file by name.
        
        Raises:
            KeyError: Raised when the model is not found.
        """
        return self.m[name]
    
    def download(
        self, 
        to: Optional[str] = None, 
        *, 
        type: Literal["economical", "best"] = "economical"
    ) -> None:
        """Download the model.
        
        Args:
            to (str, optional): Save file path.
            type (Literal["economical", "best"]): Model type.
        """
        file: ModelFile = getattr(self, type)
        file.download(to)

    def __repr__(self):
        return f"FileCollection(best={self.most_capable}, +{len(self.all) - 1})"

    def __str__(self):
        return self.__repr__()

    def __len__(self) -> int:
        return len(self.all)

class ModelFile:
    """A model file."""
    __slots__ = ("f",)
    f: dict

    def __init__(self, f: dict):
        self.f = f

    @property
    def name(self) -> str:
        return self.f['name']

    @property
    def url(self) -> str:
        """Raw file URL."""
        return self.f['url']

    @property
    def size(self) -> int:
        """Size in bytes."""
        return self.f['sizeBytes']

    @property
    def quantization(self) -> str:
        """Quantizaton.
        
        Ex. Q4_K_S
        """
        return self.f['quantization']

    @property
    def format(self) -> Literal['ggml', 'gguf']:
        """File format.

        One of:
        - ggml
        - gguf (latest, recommended)
        """
        return self.f['format']

    @property
    def publisher(self) -> dict:
        """Publisher data in dict.

        Has keys:
        - name: str
        - socialUrl: str
        """
        return self.f['publisher']

    def download(self, to: Optional[str] = None) -> None:
        """Download the model.

        Args:
            to (str, optional): The file destination.
        """
        DOWNLOAD(url=self.url, to=to or (self.name + '.' + self.format))

    def __repr__(self):
        return (
            f"ModelFile(name={self.name!r}, size={self.size}, url='{self.url[:30]}…')"
        )

    def __str__(self):
        return self.__repr__()

