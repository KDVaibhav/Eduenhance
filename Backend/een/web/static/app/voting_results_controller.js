/* Compiled file, do net edit */


/* File: ./een/web\blueprints\session\js\stages\voting_results_controller.js */

/* Voting Results Stage Controller
 *
 * param session: session
 */
function VotingResultsStageController(session) {

    function register() {
        $(".vote-details").popover({ trigger: "hover" })
    }

    function setState(value) {
        state = value
    }

    function view() {
        return Object.assign(state, {
            isPasses: state.status == "pass",
            isFailed: state.status == "fail",
            isTied: state.status == "tie",
            isFinalVote: state.type == "final"
        })
    }

    var state = null

    return { view, setState, register }
}
