"""Module containing the Sheet class.

This module provides the Sheet class, which represents a single sheet in a gauged knitting configuration.
A sheet maintains records of loop positions and provides access to needles that belong to the sheet based on the gauge spacing.

The Sheet class is fundamental to multi-sheet knitting operations,
where different parts of the knitting process are organized across multiple virtual sheets that correspond to different needle positions in a gauged pattern.
"""

from __future__ import annotations

from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.needles.Needle import Needle, Needle_Specification
from virtual_knitting_machine.machine_components.needles.Sheet_Identifier import Sheet_Identifier
from virtual_knitting_machine.machine_components.needles.Slider_Needle import Slider_Needle


class Sheet:
    """Record of the position of loops on a sheet defined by the current gauging schema.

    A Sheet represents one layer in a multi-sheet knitting configuration, where needles are organized according to a gauge pattern.
    Each sheet maintains a record of which needles currently hold loops and provides methods to access needles that belong to this particular sheet.

    The sheet system allows for complex knitting patterns where different operations are performed on different subsets of needles in a structured, repeating pattern based on the gauge value.

    Attributes:
        knitting_machine (Knitting_Machine): The knitting machine that this sheet operates on.
        loop_record (dict[int, tuple[bool, bool]]): Dictionary mapping in-sheet needle positions to tuples indicating whether loops are recorded on the front and back needles at that position.
    """

    def __init__(self, sheet_number: int, gauge: int, knitting_machine: Knitting_Machine) -> None:
        """Initialize a sheet with the specified number, gauge, and knitting machine.

        Creates a new sheet that will manage a subset of needles on the knitting machine according to the gauge pattern. The sheet records the initial state of all needles that belong to it.

        Args:
            sheet_number (int): The index of this sheet within the gauge configuration. Must be non-negative and less than the gauge value.
            gauge (int): The gauge value that determines the spacing pattern for needle organization. Must be positive.
            knitting_machine (Knitting_Machine): The knitting machine instance that this sheet will manage needles for.

        Raises:
            Sheet_Value_Exception: If sheet_number is negative or greater than or equal to the gauge value.
        """
        self.knitting_machine: Knitting_Machine = knitting_machine
        self.sheet_id: Sheet_Identifier = Sheet_Identifier(sheet_number, gauge)
        # in-sheet needle position -> Recorded loop on Front, Recorded loop on Back
        self.loop_record: dict[int, tuple[bool, bool]] = {f.position: (f.has_loops, b.has_loops) for f, b in zip(self.front_needles(), self.back_needles(), strict=False)}

    @property
    def sheet(self) -> int:
        """
        Returns:
            int: The position of the sheet in the gauge.
        """
        return self.sheet_id.sheet

    @property
    def gauge(self) -> int:
        """

        Returns:
            int: The number of active sheets.
        """
        return self.sheet_id.gauge

    def record_needle(self, needle: Needle_Specification) -> None:
        """Record the state of the given sheet needle and its opposite needle.

        Updates the loop record for the specified sheet needle position by recording the current loop state of both the front and back needles at that position.

        Args:
            needle (Sheet_Needle): The sheet needle to record the state of. Must be a valid sheet needle that belongs to this sheet.

        Raises:
            ValueError: The given needle does not belong to this sheet.

        Note:
            This method records the state of both the specified needle and its opposite bed counterpart, maintaining consistency in the loop record.
        """
        actual_needle = self.knitting_machine[needle]
        if actual_needle.sheet != self.sheet:
            raise ValueError(f"{self} does not contain needle {actual_needle}")
        opposite_needle = self.knitting_machine[actual_needle.opposite()]
        if actual_needle.is_front:
            self.loop_record[needle.position] = actual_needle.has_loops, opposite_needle.has_loops
        else:
            self.loop_record[needle.position] = opposite_needle.has_loops, actual_needle.has_loops

    def record_sheet(self) -> None:
        """Record the loop locations for needles in the sheet given the current state of the knitting machine.

        Updates the entire loop record for this sheet by examining the current state of all needles that belong to the sheet.
        This method provides a way to synchronize the sheet's record with the actual machine state.

        Note:
            This operation examines all needle positions in the sheet and updates the loop record accordingly.
            It's useful after operations that may have changed the loop distribution across the sheet.
        """
        self.loop_record = {f.position: (f.has_loops, b.has_loops) for f, b in zip(self.front_needles(), self.back_needles(), strict=False)}

    def get_matching_needle_on_sheet(self, other_needle: int | Needle_Specification) -> Needle:
        """
        Args:
            other_needle (int | Needle_Specification): The position on the machine bed (int) or needle specification of the needle in another sheet to find in this sheet.

        Returns:
            Needle: A needle belonging to this sheet at the same position of the given needle in its sheet, with matching characteristics.

        Notes:
            Providing an int for the other needle will result in a front-bed needle.
        """
        actual_needle = self.knitting_machine.get_specified_needle(is_front=True, position=other_needle) if isinstance(other_needle, int) else self.knitting_machine[other_needle]
        if actual_needle.sheet == self.sheet:
            return actual_needle
        else:
            pos_by_sheet = Needle.needle_position_from_sheet_and_gauge(actual_needle.position_in_sheet, self.sheet, self.gauge)
            return self.knitting_machine.get_specified_needle(actual_needle.is_front, pos_by_sheet, actual_needle.is_slider)

    def __eq__(self, other: object) -> bool:
        """Check equality with another Sheet or integer.

        Args:
            other (Sheet | int): The object to compare with. Can be another Sheet or an integer representing a sheet number.

        Returns:
            bool: True if the objects are equal, False otherwise.

        Note:
            When comparing with another Sheet, both sheet_number and gauge must match.
            When comparing with an integer, only the sheet_number is compared.
        """
        if isinstance(other, (Sheet, Sheet_Identifier)):
            return self.sheet == other.sheet and self.gauge == other.gauge
        elif isinstance(other, int):
            return self.sheet == other
        else:
            return False

    def front_needles(self) -> list[Needle]:
        """
        Returns:
            list[Needle]:
                The set of front bed needles on the machine that belong to this sheet, ordered by position. Needles are selected using the gauge spacing pattern starting from this sheet's offset.
        """
        machine_needles = self.knitting_machine.front_needles()
        return machine_needles[self.sheet :: self.gauge]

    def back_needles(self) -> list[Needle]:
        """
        Returns:
            list[Needle]:
                The set of back bed needles on the machine that belong to this sheet, ordered by position. Needles are selected using the gauge spacing pattern starting from this sheet's offset.
        """
        machine_needles = self.knitting_machine.back_needles()
        return machine_needles[self.sheet :: self.gauge]

    def front_sliders(self) -> list[Slider_Needle]:
        """
        Returns:
            list[Slider_Needle]:
                The set of front slider needles on the machine that belong to this sheet, ordered by position. Needles are selected using the gauge spacing pattern starting from this sheet's offset.
        """
        machine_needles = self.knitting_machine.front_sliders()
        return machine_needles[self.sheet :: self.gauge]

    def back_sliders(self) -> list[Slider_Needle]:
        """
        Returns:
            list[Slider_Needle]:
                The set of back slider needles on the machine that belong to this sheet, ordered by position. Needles are selected using the gauge spacing pattern starting from this sheet's offset.
        """
        machine_needles = self.knitting_machine.back_sliders()
        return machine_needles[self.sheet :: self.gauge]

    def front_loops(self) -> list[Needle]:
        """
        Returns:
            list[Needle]: The list of front bed needles that belong to this sheet and currently hold loops, ordered by position.
        """
        return [n for n in self.front_needles() if n.has_loops]

    def back_loops(self) -> list[Needle]:
        """
        Returns:
            list[Needle]: The list of back bed needles that belong to this sheet and currently hold loops, ordered by position.
        """
        return [n for n in self.back_needles() if n.has_loops]

    def front_slider_loops(self) -> list[Slider_Needle]:
        """
        Returns:
            list[Slider_Needle]: The list of front bed slider needles that belong to this sheet and currently hold loops, ordered by position.
        """
        return [n for n in self.front_sliders() if n.has_loops]

    def back_slider_loops(self) -> list[Slider_Needle]:
        """
        Returns:
            list[Slider_Needle]: The list of back bed slider needles that belong to this sheet and currently hold loops, ordered by position.
        """
        return [n for n in self.back_sliders() if n.has_loops]

    def all_needles(self) -> list[Needle]:
        """
        Returns:
            list[Needle]: List of all needles on the sheet with front bed needles given first, followed by back bed needles, all ordered by position within their respective beds.
        """
        return [*self.front_needles(), *self.back_needles()]

    def all_sliders(self) -> list[Slider_Needle]:
        """
        Returns:
            list[Slider_Needle]: List of all slider needles on the sheet with front bed sliders given first, followed by back bed sliders, all ordered by position within their respective beds.
        """
        return [*self.front_sliders(), *self.back_sliders()]

    def all_loops(self) -> list[Needle]:
        """
        Returns:
            list[Needle]: List of all loop-holding needles on the sheet with front bed needles given first, followed by back bed needles, all ordered by position within their respective beds.
        """
        return [*self.front_loops(), *self.back_loops()]

    def all_slider_loops(self) -> list[Slider_Needle]:
        """
        Returns:
            list[Slider_Needle]:
                List of all loop-holding slider needles on the sheet with front bed sliders given first, followed by back bed sliders, all ordered by position within their respective beds.
        """
        return [*self.front_slider_loops(), *self.back_slider_loops()]

    def __str__(self) -> str:
        return f"Sheet {self.sheet} at gauge {self.gauge}"

    def __repr__(self) -> str:
        return str(self)
