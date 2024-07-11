/* Compiled file, do net edit */


/* File: ./een/web\blueprints\session\js\stages\simple_controller.js */

/* Simple stage controller
 * Provides basic functionality
 * param session: session
 */
function SimpleStageController(session) {

    function setState(value) {
        state = value
    }

    function view() {
        return state
    }

    // Private members

    var state = null

    return { view, setState }
}
