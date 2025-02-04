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
    // TODO =========== CAMBIO HERENCIA - OLD =============
    // if (this.popover.isOpen) {
    //     return;
    // }
    // const popoverTarget = ev.target.closest(".o_gantt_pill_wrapper");
    // this.popover.open(popoverTarget, this.getPopoverProps(pill));
    // TODO =========== NEW =============
    this.model.mutex.exec(
      () => this.props.openDialog({ resId: pill.record.id }) // (canEdit is also considered in openDialog)
    );
    // TODO =========== END    =============
  },

  getDisplayName(pill) {
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
      // TODO =========== CAMBIO HERENCIA - OLD =============
      // labelElements.push(
      //   startDate.toFormat("t"),
      //   `${stopDate.toFormat("t")} (${durationStr})`
      // );
     // TODO =========== NEW =============
      labelElements.push(
        `(${durationStr})`
      );
      // TODO =========== END    =============
    }

    // Original Display Name
    if (scaleId !== "month" || !record.allocated_hours || spanAccrossDays) {
      labelElements.push(record.display_name);
    }

    return labelElements.filter((el) => !!el).join(" - ");
  },

  getPillFromGroup(group, maxAggregateValue, consolidate) {
    const { excludeField, field, maxValue } = this.model.metaData.consolidationParams;
    
    const minColor = 215;
    const maxColor = 100;
    const newPill = {
        id: `__pill__${this.nextPillId++}`,
        level: 0,
        aggregateValue: group.aggregateValue,
        grid: group.grid,
        // TODO =========== CAMBIO HERENCIA - NEW =============
        pills_length: group.pills.length,
        recourse_plannable_hours: group.pills[0].record.x_resourse_plannable_hours
        // TODO =========== END    =============
    };

    // Enrich the aggregates with consolidation data
    if (consolidate && field) {
        newPill.consolidationValue = 0;
        for (const pill of group.pills) {
            if (!pill.record[excludeField]) {
                newPill.consolidationValue += pill.record[field];
            }
        }
        newPill.consolidationMaxValue = maxValue;
        newPill.consolidationExceeded =
            newPill.consolidationValue > newPill.consolidationMaxValue;
    }

    if (consolidate && maxValue) {
        const status = newPill.consolidationExceeded ? "danger" : "success";
        newPill.className = `bg-${status} border-${status}`;
        newPill.displayName = newPill.consolidationValue;
    } else {
        const color =
            minColor -
            Math.round((newPill.aggregateValue - 1) / maxAggregateValue) *
                (minColor - maxColor);
        newPill.style = `background-color:rgba(${color},${color},${color},0.6)`;
        // TODO =========== CAMBIO HERENCIA - OLD =============
        //newPill.displayName = this.getGroupPillDisplayName(newPill);
        // TODO =========== NEW =============
        if(newPill.aggregateValue > newPill.recourse_plannable_hours) {
          newPill.className = 'warning_red';
        } else {
          newPill.className = 'transparente';
        }
        newPill.displayName = `${newPill.pills_length} - ${this.getGroupPillDisplayName(newPill)}`;
        // TODO =========== END    =============
    }

    return newPill;
  },

  getPills() {
    const { records } = this.model.data;
    const { dateStartField } = this.model.metaData;
    const pills = [];
    // TODO =========== CAMBIO HERENCIA - NEW =============
    let date_now = new Date();
    date_now.setHours(0, 0, 0, 0);
    const userTimezoneOffset = date_now.getTimezoneOffset() * 60000;
    const d = new Date(date_now.getTime() - userTimezoneOffset);
    // TODO =========== END    =============
    for (const record of records) {
        const pill = this.getPill(record);
        // TODO =========== CAMBIO HERENCIA - NEW =============
        if(this.env.searchModel.resModel === 'planning.slot'){
          pill.record.color = Number(pill.record.color);
        }
        // TODO =========== END    =============
        pills.push(this.enrichPill(pill));
    }
    // sorting cannot be done when fetching data --> the snapping of pills breaks order
    return pills.sort(
        (p1, p2) =>
            p1.grid.column[0] - p2.grid.column[0] ||
            p1.record[dateStartField] - p2.record[dateStartField]
    );
  }


});
