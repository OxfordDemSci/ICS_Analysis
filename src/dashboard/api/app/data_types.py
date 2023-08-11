from dataclasses import dataclass
from typing import Union

from reportlab.lib.enums import TA_CENTER, TA_LEFT  # type: ignore
from reportlab.lib.styles import (ParagraphStyle,  # type: ignore
                                  getSampleStyleSheet)

from app import db
from app.models import ICS, UOA, Countries, Funder, Topics


@dataclass
class ThresholdType:
    value: float  # type: ignore

    @property  # type: ignore
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, new_value: float) -> None:
        if not 0 <= new_value <= 1:
            raise ValueError("Threshold must be float between 0 and 1")
        self._value = new_value


@dataclass
class TopicType:
    value: str | None = None  # type: ignore

    @property  # type: ignore
    def value(self) -> Union[str, None]:
        return self._value

    @value.setter
    def value(self, new_value: str | None) -> None:
        values = db.session.query(Topics.topic_name).distinct().all()
        if new_value is None or new_value in [x[0] for x in values]:
            self._value = new_value
        else:
            raise ValueError(f"Topic invalid - {new_value}")


@dataclass
class PostCodeAreaType:
    value: str | None = None  # type: ignore

    @property  # type: ignore
    def value(self) -> Union[str, None]:
        return self._value

    @value.setter
    def value(self, new_value: str | None) -> None:
        values = db.session.query(ICS.postcode).distinct().all()
        if new_value is None or new_value in [x[0] for x in values]:
            self._value = new_value
        else:
            raise ValueError(f"Postcode invalid - {new_value}")


@dataclass
class BeneficiaryType:
    value: str | None = None  # type: ignore

    @property  # type: ignore
    def value(self) -> Union[str, None]:
        return self._value

    @value.setter
    def value(self, new_value: str | None) -> None:
        values = db.session.query(Countries.country).distinct().all()
        if new_value is None or new_value in [x[0] for x in values]:
            self._value = new_value
        else:
            raise ValueError(f"Beneficiary invalid - {new_value}")


@dataclass
class UOAType:
    value: str | None = None  # type: ignore

    @property  # type: ignore
    def value(self) -> Union[str, None]:
        return self._value

    @value.setter
    def value(self, new_value: str | None) -> None:
        values_panel = db.session.query(UOA.assessment_panel).distinct().all()
        values_group = db.session.query(UOA.assessment_group).distinct().all()
        if new_value is None or new_value in [x[0] for x in values_panel] or new_value in [x[0] for x in values_group]:
            self._value = new_value
        else:
            raise ValueError(f"UOA invalid - {new_value}")


@dataclass
class FunderType:
    value: str | None = None  # type: ignore

    @property  # type: ignore
    def value(self) -> Union[str, None]:
        return self._value

    @value.setter
    def value(self, new_value: str | None) -> None:
        values = db.session.query(Funder.funder).distinct().all()
        if new_value is None or new_value in [x[0] for x in values]:
            self._value = new_value
        else:
            raise ValueError(f"Funder invalid - {new_value}")


title_style = ParagraphStyle(
    "Title",
    parent=getSampleStyleSheet()["Title"],
    alignment=TA_CENTER,
    fontName="Helvetica-Bold",  # Replace with your desired font name
    fontSize=24,
)


subtitle_style = ParagraphStyle(
    "Heading3",
    parent=getSampleStyleSheet()["Heading3"],
    alignment=TA_LEFT,
    fontName="Helvetica",  # Replace with your desired font name
    fontSize=18,
    underlineColor="black",
    underlineWidth=1,
)

body_text_style = ParagraphStyle(
    "BodyStyle",
    parent=getSampleStyleSheet()["Normal"],
    alignment=TA_LEFT,
    fontName="Helvetica",
    fontSize=12,
)

subtitle_style_center = ParagraphStyle(
    "Heading3",
    parent=getSampleStyleSheet()["Heading3"],
    alignment=TA_CENTER,
    fontName="Helvetica",  # Replace with your desired font name
    fontSize=18,
    underlineColor="black",
    underlineGap=2,
    underlineWidth=1,
)

small_centered_style = ParagraphStyle(
    "SmallCentered",
    parent=getSampleStyleSheet()[
        "Normal"
    ],  # You can replace 'Normal' with any other style name from the style sheet
    fontSize=8,  # Adjust the font size as needed
    alignment=TA_CENTER,
    fontName="Helvetica-Bold",
)


styles_map = {
    "title": title_style,
    "subtitle": subtitle_style,
    "subtitle_center": subtitle_style_center,
    "body": body_text_style,
    "footnote": small_centered_style,
}
