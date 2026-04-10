/** @odoo-module */

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
import { ChartRenderer } from "./chart_renderer/chart_renderer"
import { loadJS } from "@web/core/assets"
const { Component, onWillStart, useRef, onMounted } = owl

export class TFGDashboard extends Component {
    setup(){

    }
}

TFGDashboard.template = "tfg_power_bi_assistant.dashboard"
TFGDashboard.components = { KpiCard, ChartRenderer }

registry.category("actions").add("tfg_power_bi_assistant.dashboard", TFGDashboard)