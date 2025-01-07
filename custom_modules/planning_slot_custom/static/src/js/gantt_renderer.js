/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { GanttRenderer } from "@web_gantt/gantt_renderer";
import { omit } from "@web/core/utils/objects";
const { DateTime } = luxon;
import { computeRange } from "@web_gantt/gantt_model";
import { formatFloatTime } from "@web/views/fields/formatters";

patch(GanttRenderer.prototype, {
  async setup() {
    super.setup(); // By using the super function, we can execute all parent functions along with ours.
  },

  onPillClicked(ev, pill) {
    this.model.mutex.exec(
      () => this.props.openDialog({ resId: pill.record.id }) // (canEdit is also considered in openDialog)
    );
  },

  getDisplayName(pill) {
    debugger;
    const { computePillDisplayName, dateStartField, dateStopField, scale } =
      this.model.metaData;
    const { id: scaleId } = scale;
    const { record } = pill;

    if (!computePillDisplayName) {
      return record.display_name;
    }

    const startDate = record[dateStartField];
    const stopDate = record[dateStopField];
    const yearlessDateFormat = omit(DateTime.DATE_SHORT, "year");

    const spanAccrossDays =
      stopDate.startOf("day") > startDate.startOf("day") &&
      startDate.endOf("day").diff(startDate, "hours").toObject().hours >= 3 &&
      stopDate.diff(stopDate.startOf("day"), "hours").toObject().hours >= 3;
    const spanAccrossWeeks =
      computeRange("week", stopDate).start >
      computeRange("week", startDate).start;
    const spanAccrossMonths =
      stopDate.startOf("month") > startDate.startOf("month");

    /** @type {string[]} */
    const labelElements = [];

    // Start & End Dates
    if (scaleId === "year" && !spanAccrossDays) {
      labelElements.push(startDate.toLocaleString(yearlessDateFormat));
    } else if (
      (scaleId === "day" && spanAccrossDays) ||
      (scaleId === "week" && spanAccrossWeeks) ||
      (scaleId === "month" && spanAccrossMonths) ||
      (scaleId === "year" && spanAccrossDays)
    ) {
      labelElements.push(startDate.toLocaleString(yearlessDateFormat));
      labelElements.push(stopDate.toLocaleString(yearlessDateFormat));
    }

    // Start & End Times
    if (
      record.allocated_hours &&
      !spanAccrossDays &&
      ["week", "month"].includes(scaleId)
    ) {
      const durationStr = formatFloatTime(record.allocated_hours, {
        noLeadingZeroHour: true,
      }).replace(/(:00|:)/g, "h");
      // labelElements.push(
      //   startDate.toFormat("t"),
      //   `${stopDate.toFormat("t")} (${durationStr})`
      // );
      labelElements.push(
        `(${durationStr})`
      );
    }

    // Original Display Name
    if (scaleId !== "month" || !record.allocated_hours || spanAccrossDays) {
      labelElements.push(record.display_name);
    }

    return labelElements.filter((el) => !!el).join(" - ");
  },
});
