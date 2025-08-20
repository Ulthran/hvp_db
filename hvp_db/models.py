from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import Date, Enum, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


def init_engine(url: str, *, echo: bool = False):
    """Create an engine and initialize the database schema."""
    engine = create_engine(url, echo=echo)
    Base.metadata.create_all(engine)
    return engine


def get_session_maker(url: str, *, echo: bool = False):
    """Return a configured :class:`sessionmaker` for the database."""
    engine = init_engine(url, echo=echo)
    return sessionmaker(bind=engine)


# Enumerations
AnatomicalSite = Enum(
    "np_swab",
    "buccal_swab",
    "tongue_dorsum",
    "saliva",
    "op_wash",
    "dental_plaque",
    "serum",
    "whole_blood",
    "periglottic",
    "bal_a",
    "bal_b",
    "bronch_prewash",
    "endobronch_brush_l",
    "endobronch_brush_r",
    "stool",
    name="anatomical_site",
)

LabOrigin = Enum("wu", "teles", "zemel", "collman", name="lab_origin")

StorageBuffer = Enum(
    "neat", "bead_beater", "vtm", "pbs", "zymo_shield", "oral_cocktail", name="storage_buffer"
)

PrepType = Enum(
    "metagenomic",
    "16s",
    "virome_prep_guanxiang",
    "virome_prep_colin_hill",
    "virome_prep_matthijnssens",
    name="prep_type",
)

ExtractionType = Enum("none", "qiaamp_viral_rna_minikit", "allprep", name="extraction_type")
RNAType = Enum("powersoil_pro", "allprep", name="rna_type")
DNAType = Enum("powersoil_pro", "allprep", name="dna_type")
AmplifiedType = Enum(
    "none", "wta2", "pta", "malbac", "genomephi", name="amplified_type"
)

LibraryType = Enum(
    "nextera_xt",
    "pta",
    "ont_rapid_pcr_barcoding",
    "ont_rapid_sequencing_kit",
    "pacbio_amplifi",
    "pacbio_hifi",
    name="library_type",
)

BarcodeSet = Enum("A", "B", "C", "D", name="barcode_set")
SampleUse = Enum("experiment", "pilot", name="sample_use")

SequencePlatform = Enum(
    "miseq_i100", "nextseq", "miseq", "miniseq", "minion", "pacbio", name="sequence_platform"
)

SequenceGroup = Enum("bushman", "moustafa", name="sequence_group")


class Sample(Base):
    """Table describing the processing history of a sample."""

    __tablename__ = "samples"

    sample_id: Mapped[str] = mapped_column(String(8), primary_key=True)
    sample_id_alias: Mapped[Optional[str]] = mapped_column(String(32))
    participant_id: Mapped[str] = mapped_column(String(16), nullable=False)
    anatomical_site: Mapped[str] = mapped_column(AnatomicalSite, nullable=False)
    lab_origin: Mapped[Optional[str]] = mapped_column(LabOrigin)
    date_collected: Mapped[date] = mapped_column(Date, nullable=False)
    date_hvp_custody: Mapped[Optional[date]] = mapped_column(Date)
    storage_buffer: Mapped[str] = mapped_column(StorageBuffer, nullable=False)
    raw_consumed_date: Mapped[Optional[date]] = mapped_column(Date)
    raw_location_box: Mapped[Optional[str]] = mapped_column(String(64))
    raw_location_plate: Mapped[Optional[str]] = mapped_column(String(64))
    raw_location_plate_pos: Mapped[Optional[str]] = mapped_column(String(4))

    prep_type: Mapped[Optional[str]] = mapped_column(PrepType)
    prep_date: Mapped[Optional[date]] = mapped_column(Date)
    prep_person: Mapped[Optional[str]] = mapped_column(String(64))
    prep_consumed_date: Mapped[Optional[date]] = mapped_column(Date)
    prep_location_box: Mapped[Optional[str]] = mapped_column(String(64))
    prep_location_plate: Mapped[Optional[str]] = mapped_column(String(64))
    prep_location_plate_pos: Mapped[Optional[str]] = mapped_column(String(4))

    extraction_type: Mapped[Optional[str]] = mapped_column(ExtractionType)
    extraction_person: Mapped[Optional[str]] = mapped_column(String(64))
    extraction_consumed_date: Mapped[Optional[date]] = mapped_column(Date)
    extraction_location_box: Mapped[Optional[str]] = mapped_column(String(64))
    extraction_location_plate: Mapped[Optional[str]] = mapped_column(String(64))
    extraction_location_plate_pos: Mapped[Optional[str]] = mapped_column(String(4))

    extraction_rna_type: Mapped[Optional[str]] = mapped_column(RNAType)
    extraction_rna_person: Mapped[Optional[str]] = mapped_column(String(64))
    extraction_rna_consumed_date: Mapped[Optional[date]] = mapped_column(Date)
    extraction_rna_location_box: Mapped[Optional[str]] = mapped_column(String(64))
    extraction_rna_location_plate: Mapped[Optional[str]] = mapped_column(String(64))
    extraction_rna_location_plate_pos: Mapped[Optional[str]] = mapped_column(String(4))

    extraction_dna_type: Mapped[Optional[str]] = mapped_column(DNAType)
    extraction_dna_person: Mapped[Optional[str]] = mapped_column(String(64))
    extraction_dna_consumed_date: Mapped[Optional[date]] = mapped_column(Date)
    extraction_dna_location_box: Mapped[Optional[str]] = mapped_column(String(64))
    extraction_dna_location_plate: Mapped[Optional[str]] = mapped_column(String(64))
    extraction_dna_location_plate_pos: Mapped[Optional[str]] = mapped_column(String(4))

    amplified_type: Mapped[Optional[str]] = mapped_column(AmplifiedType)
    amplified_person: Mapped[Optional[str]] = mapped_column(String(64))
    amplified_consumed_date: Mapped[Optional[date]] = mapped_column(Date)
    amplified_location_box: Mapped[Optional[str]] = mapped_column(String(64))
    amplified_location_plate: Mapped[Optional[str]] = mapped_column(String(64))
    amplified_location_plate_pos: Mapped[Optional[str]] = mapped_column(String(4))

    library_type: Mapped[Optional[str]] = mapped_column(LibraryType)
    library_date: Mapped[Optional[date]] = mapped_column(Date)
    library_person: Mapped[Optional[str]] = mapped_column(String(64))
    library_consumed_date: Mapped[Optional[date]] = mapped_column(Date)
    library_location_box: Mapped[Optional[str]] = mapped_column(String(64))
    library_location_plate: Mapped[Optional[str]] = mapped_column(String(64))
    library_location_plate_pos: Mapped[Optional[str]] = mapped_column(String(4))
    library_barcode_set: Mapped[Optional[str]] = mapped_column(BarcodeSet)
    library_barcode_position: Mapped[Optional[str]] = mapped_column(String(4))
    library_barcode_i5: Mapped[Optional[str]] = mapped_column(String(32))
    library_barcode_i7: Mapped[Optional[str]] = mapped_column(String(32))

    sample_use: Mapped[str] = mapped_column(SampleUse, nullable=False)
    date_sequenced: Mapped[Optional[date]] = mapped_column(Date)
    sequence_platform: Mapped[Optional[str]] = mapped_column(SequencePlatform)
    sequence_chemistry: Mapped[Optional[str]] = mapped_column(String(64))
    sequence_group: Mapped[Optional[str]] = mapped_column(SequenceGroup)
    sequence_run_id: Mapped[Optional[str]] = mapped_column(String(64))
    sample_deviation: Mapped[Optional[str]] = mapped_column(Text)
