//
//     Copyright © 2011-2022 Cambridge Intelligence Limited.
//     All rights reserved.
//
//     Sample Code
//!    Filter geo-coded data to see hidden connections.

import data from './filtermap-data.js';

let chart;
let filterInProgress = false;
let refilter = false;
let minFlightVolume = 0;

// Get UI objects
const fgSelectCheckbox = document.getElementById('fgSelect');

const flightVolumeSlider = document.getElementById('flightVolumeSlider');

const checkboxNodeList = document.getElementsByClassName('airlineCheckbox');
const selectAllButton = document.getElementById('selectAll');
const selectNoneButton = document.getElementById('selectNone');
const selectInvertButton = document.getElementById('selectInvert');

const mapOn = document.getElementById('mapOn');
const mapOff = document.getElementById('mapOff');

// returns an object with airline IDs as keys and bool values indicating if its checkbox is checked
function getCheckboxStatuses() {
    const checkedList = {};
    const elementList = Array.from(checkboxNodeList);
    elementList.forEach((element) => {
        checkedList[element.id] = element.checked;
    });
    return checkedList;
}

function filterChart() {
    // Don't start a new filter if one is currently running but
    // ensure it refilters with the updated settings once the current filter has finished
    refilter = filterInProgress;
    if (refilter) {
        return;
    }
    filterInProgress = true;
    const checked = getCheckboxStatuses(checkboxNodeList);

    chart.filter(item => ((item.d.n >= minFlightVolume) && checked[item.d.carrier]), { type: 'link' })
        .then(() => {
            filterInProgress = false;
            if (refilter) {
                filterChart();
            } else if (!chart.map().isShown()) {
                chart.layout();
            }
        });
}

function onSelectionChange() {
    const selectedItems = chart.selection();
    if (selectedItems.length > 0 && fgSelectCheckbox.checked) {
        const neighbours = chart.component.graph().neighbours(selectedItems);
        const idsToForeground = selectedItems.concat(neighbours.links);
        // foreground only links which will automatically foreground nodes at end of those links
        chart.foreground(item => idsToForeground.includes(item.id), { type: 'link' });
    } else {
        // foreground everything
        chart.foreground(() => true);
    }
    // focus back on the slider to stop Edge requiring 2 taps
    flightVolumeSlider.focus();
}

function updateAirlineCheckboxes(updateFn) {
    const elementList = Array.from(checkboxNodeList);
    elementList.forEach(updateFn);
}

function addEventListeners() {
    // updates slider text when moved
    flightVolumeSlider.addEventListener('input', () => {
        const sliderValue = flightVolumeSlider.value;
        document.getElementById('sliderDisplayValue').innerHTML = ` ${sliderValue}`;
    });
    // does all filtering once slider has changed and been released
    flightVolumeSlider.addEventListener('change', () => {
        minFlightVolume = flightVolumeSlider.value;
        filterChart();
        onSelectionChange();
    });
    flightVolumeSlider.addEventListener('mouseup', () => {
        if (minFlightVolume !== flightVolumeSlider.value) {
            minFlightVolume = flightVolumeSlider.value;
            filterChart();
            onSelectionChange();
        }
    });

    selectAllButton.addEventListener('click', () => {
        updateAirlineCheckboxes((checkbox) => {
            checkbox.checked = true;
        });
        filterChart();
    });

    selectNoneButton.addEventListener('click', () => {
        updateAirlineCheckboxes((checkbox) => {
            checkbox.checked = false;
        });
        filterChart();
    });

    selectInvertButton.addEventListener('click', () => {
        updateAirlineCheckboxes((checkbox) => {
            checkbox.checked = !checkbox.checked;
        });
        filterChart();
    });

    Array.from(checkboxNodeList).forEach((checkbox) => {
        checkbox.addEventListener('change', filterChart);
    });

    fgSelectCheckbox.addEventListener('change', onSelectionChange);

    mapOn.addEventListener('click', chart.map().show);
    mapOff.addEventListener('click', chart.map().hide);
}

// Enable/Disable filters, used on transition start.
function disableUiControls(disabledVal) {
    updateAirlineCheckboxes((checkbox) => { checkbox.disabled = disabledVal; });
    flightVolumeSlider.disabled = disabledVal;
    selectAllButton.disabled = disabledVal;
    selectNoneButton.disabled = disabledVal;
    selectInvertButton.disabled = disabledVal;
    fgSelectCheckbox.disabled = disabledVal;
}

function mapModeChange({ type }) {
    // Disable UI on map transition start and enable it on end
    if (type === 'showstart' || type === 'hidestart') {
        mapOn.classList.toggle('active');
        mapOff.classList.toggle('active');
        disableUiControls(true);
    } else if (type === 'showend' || type === 'hideend') {
        disableUiControls(false);
    }
}

function klReady() {
    // data is defined in filtermap-data.js
    chart.load(data);
    chart.layout();

    const southwest = L.latLng(-30, -210);
    const northeast = L.latLng(80, -30);

    const mapOptions = {
        animate: true,
        time: 800,
        transition: 'layout',
        leaflet: {
            maxZoom: 10,
            minZoom: 3,
            // Limit map panning and zoom to be roughly around USA
            maxBounds: L.latLngBounds(southwest, northeast),
            maxBoundsViscosity: 1,
        },
    };

    chart.map().options(mapOptions);

    chart.on('selection-change', onSelectionChange);
    chart.on('map', mapModeChange);

    addEventListeners();
}

async function loadKeyLines() {
    KeyLines.promisify();


    const options = {
        logo: 'images/Logo.png',
        hover: 100,
        handMode: true,
    };

    chart = await KeyLines.create({
        container: 'klchart',
        options,
    });


    klReady();
}

window.addEventListener('DOMContentLoaded', loadKeyLines);