/* FieldCommand IMS — Common Objective Library (shared)
 *
 * One source of truth for the "Common Objective Library" pick-list used on the
 * ICS-202 form (ics-form.html), the Command page (ics/command.html), and the
 * Event Templates editor (event_templates.html). Edit the list HERE only.
 *
 * Any <select class="obj-library"> on the page is auto-filled on load. The
 * pick-list only PRE-FILLS text — operators can always edit a picked objective
 * or type an objective by hand instead.
 */
window.FC_COMMON_OBJECTIVES = [
  ['Life Safety', [
    'Ensure the life safety of all responders and the public as the first priority',
    'Establish and maintain accountability of all incident personnel',
    'Provide emergency medical support for all activated personnel',
    'Identify and mitigate all safety hazards in the operational area',
    'Establish and maintain a safe work environment for all responders',
    'Conduct welfare checks on all isolated or vulnerable populations in the affected area',
    'Establish decontamination procedures for all personnel exiting the hot zone',
    'Ensure no responder works more than [hours] hours without adequate rest per the work-rest ratio',
    'Establish a personnel rehabilitation area for rest, hydration, and medical monitoring',
  ]],
  ['Communications', [
    'Establish and maintain communications with all field units on the primary tactical channel',
    'Maintain a continuous communications link with the County EOC',
    'Provide Winlink email capability for formal message traffic throughout the operational period',
    'Establish backup communications via HF on [frequency] MHz in the event of VHF failure',
    'Monitor all assigned radio channels and log all significant traffic in ICS-309',
    'Establish and maintain a net control station at the Incident Command Post',
    'Provide communications coverage for all assigned geographic sectors',
    'Test and verify all assigned radio frequencies before the start of the operational period',
    'Coordinate radio frequencies with all mutual aid agencies operating on the incident',
  ]],
  ['Resource Management', [
    'Check in all incoming resources and maintain an accurate resource status board',
    'Coordinate logistics for food, water, fuel, and shelter for all activated personnel',
    'Identify and request additional resources needed for the next operational period',
    'Demobilize all resources no longer needed and document demobilization in ICS-221',
    'Establish and maintain a staging area for incoming resources at [location]',
    'Assign all activated personnel to a Division or Group before the start of operations',
    'Track and report resource status changes to the Resources Unit every [interval]',
  ]],
  ['Incident Command', [
    'Establish a unified command structure with all agencies operating on this incident',
    'Complete and distribute the Incident Action Plan before the start of each operational period',
    'Conduct an operational period briefing at [time] prior to each shift change',
    'Maintain a complete and accurate incident documentation file in accordance with ICS standards',
    'Conduct a transition briefing with incoming personnel at each shift change',
    'Provide situation status updates to the EOC every [interval]',
    'Establish and maintain a clear chain of command for all incident operations',
    'Implement the ICS span of control standard — no supervisor responsible for more than seven personnel',
  ]],
  ['Search & Rescue', [
    'Conduct a systematic primary search of the assigned area and report results to Operations',
    'Conduct a secondary search of all areas where primary search was interrupted or inconclusive',
    'Maintain continuous radio contact with all search teams in the field',
    'Coordinate with the Planning Section to update the search assignment map every [interval]',
    'Establish and maintain a hasty team capability for rapid response to confirmed sightings',
    'Document all search assignments and results on ICS-204 and submit to the Planning Section',
    'Coordinate canine search resources with field teams to maximize coverage efficiency',
    'Establish and maintain a command post at [location] to support all field search operations',
    'Brief all search teams on last known point, travel direction, and subject profile before deployment',
    'Ensure all field teams carry required personal protective equipment and navigation tools',
  ]],
  ['Shelter & Mass Care', [
    'Open and staff the emergency shelter at [location] to support displaced residents',
    'Coordinate registration of all shelter residents using the American Red Cross registration system',
    'Provide communications link between the shelter and the Incident Command Post',
    'Coordinate medical screening for all shelter arrivals with the Medical Unit',
    'Establish and maintain a pet-friendly shelter area separate from the main shelter population',
    'Coordinate meals and supply logistics for shelter population with the Logistics Section',
  ]],
  ['Weather & Natural Disaster', [
    'Monitor and report all significant weather observations to the Situation Unit every [interval]',
    'Provide NWS storm spotter coverage for the assigned geographic area throughout the operational period',
    'Coordinate damage assessment operations in the affected area and report findings to the Planning Section',
    'Establish contact with all affected jurisdictions and assess their communications needs',
    'Coordinate utility restoration communications with [utility company] field crews',
    'Provide ground truth confirmation of reported damage to assist NWS with warning decisions',
    'Support door-to-door welfare check operations in areas where utilities or communications are disrupted',
    'Monitor river and flood gauge readings at [location] and report to EOC every [interval]',
  ]],
  ['HazMat', [
    'Establish hot, warm, and cold zone perimeters and maintain them throughout the incident',
    'Coordinate with HazMat team to identify the released substance and determine protective actions',
    'Provide communications relay between the HazMat team in the hot zone and Incident Command',
    'Coordinate public notification and evacuation with law enforcement and local government',
    'Monitor weather conditions and adjust protective action recommendations as wind direction changes',
    'Establish a decontamination corridor and coordinate with EMS for potential patient decontamination',
  ]],
  ['Mass Casualty', [
    'Establish a triage area and begin START triage of all patients at [location]',
    'Coordinate patient distribution to receiving hospitals and maintain a patient tracking log',
    'Establish communications with all receiving hospitals and provide patient count updates every [interval]',
    'Coordinate with Logistics for additional medical supplies and equipment as needed',
    'Establish a fatality management area and coordinate with the Medical Examiner',
    'Provide communications link between EMS field units and the Medical Branch Director',
  ]],
  ['Public Information', [
    'Coordinate all public information releases through the designated Public Information Officer',
    'Establish a joint information center with all participating agencies for this incident',
    'Provide a public inquiry line and log all contacts in accordance with the communications plan',
    'Release an initial incident information summary to the public within [time] of activation',
    'Monitor social media for incident-related misinformation and coordinate corrections through the PIO',
    'Provide regular situation updates to elected officials and agency administrators throughout the incident',
    'Document all media inquiries and coordinate responses through the designated PIO',
    'Establish a family reunification center and coordinate with law enforcement for notifications',
  ]],
  ['Finance & Administration', [
    'Document all personnel time on ICS-211 and ICS-214 for cost recovery purposes',
    'Track all expenditures and procurement actions for submission to the Finance Section',
    'Obtain authorization from the Finance Section Chief before any procurement exceeding $[amount]',
    'Complete all time reports and submit to the Finance Section before demobilization',
  ]],
  ['Demobilization', [
    'Develop a demobilization plan and distribute to all sections before the end of the operational period',
    'Complete all required documentation before demobilization of any resources',
    'Conduct an after-action review with all section chiefs before closing out the incident',
    'Return all borrowed or shared equipment to the issuing agency before demobilization',
    'Ensure all ICS forms are completed, compiled, and archived in the incident documentation file',
    'Brief incoming shift or relief personnel on current status before demobilization of current shift',
    'Compile all ICS-214 activity logs and submit a consolidated report to the Documentation Unit',
    'Notify all served agencies of demobilization timeline at least [time] before release of resources',
  ]],
  ['Organization-Specific', [
    'Establish and maintain communications with the County EOC throughout the operational period',
    'Coordinate radio resources with the County Emergency Management Agency',
    'Provide RACES/ARES communications support to all served agencies requesting assistance',
    'Maintain an accurate activation roster in the FieldCommand system throughout the incident',
    'Coordinate with the ARES Emergency Coordinator for resource assignments',
    'Provide a final incident summary to the County EMA Director before demobilization',
    'Ensure all activated members are logged in the FieldCommand roster before operations begin',
    'Coordinate mutual aid communications resources with neighboring county ARES/RACES groups',
    'Submit a completed ICS-214 activity log for each activated unit before demobilization',
    'Provide written documentation of all significant events to the County EMA after the incident',
    'Test all primary and backup communication paths before declaring the activation operational',
  ]],
];

/* Fill one <select> with the library (a placeholder option + grouped options). */
window.fcFillObjectiveSelect = function (sel, placeholder) {
  if (!sel) return;
  placeholder = placeholder || '— Select a common objective to pre-fill —';
  sel.innerHTML = '';
  var ph = document.createElement('option');
  ph.value = '';
  ph.textContent = placeholder;
  sel.appendChild(ph);
  (window.FC_COMMON_OBJECTIVES || []).forEach(function (grp) {
    var og = document.createElement('optgroup');
    og.label = grp[0];
    grp[1].forEach(function (text) {
      var o = document.createElement('option');
      o.textContent = text;   // textContent = safe, no HTML injection
      og.appendChild(o);
    });
    sel.appendChild(og);
  });
};

/* Auto-fill every <select class="obj-library"> present at load. */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('select.obj-library').forEach(function (sel) {
    window.fcFillObjectiveSelect(sel, sel.getAttribute('data-placeholder') || undefined);
  });
});
