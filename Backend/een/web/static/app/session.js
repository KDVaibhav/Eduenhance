/* Compiled file, do net edit */


/* File: ./een/web/blueprints/session/js/session_chat.js */

function createChatController(controller) {

    var messagesPanel = $("#messages")
    var messageInput = $("#chat-message")

    $("#chat-message").keypress(function (e) {
        if (e.which != 13) return

        var msg = messageInput.val()
        messageInput.val("")
        say(msg)
        return false
    })

    function processMessage(data) {
        append(data)
    }

    function say(message) {
        controller.socket.emit("chat", { msg: message });
    }

    function append(data) {
        messagesPanel.append("<li>" + data["who"] + ": " + data["msg"] + "</li>")
    }

    return { processMessage, say }
}

/* File: ./een/web/blueprints/session/js/session_controller.js */

// Session controller

function createSessionController(sessionKey, sessionData) {
    me = {}

    me.sessionKey = sessionKey
    me.users = UsersPanelController(me, $("#session-users-list"), $("#session-users-line").html())
    me.chat = createChatController(me)
    me.timer = createTimerController(me)
    me.manage = createManageController(me)
    me.stage = StageController(me, $("#stage-proposal"), $("#stage-widget"))
    me.quorum = QuorumController(me)

    // info line
    me.infoLine = InfoLineController(me, $("#footer-info"))
    me.infoLine.setEndTime(new Date(sessionData.date + " " + sessionData.time_end))
    me.infoLine.setSessionTitle(sessionData.title)


    me.user = null

    function onKick(data) {
        me.socket.disconnect()
        Alerts().alert({
            title: data.title || "You have been removed from the session",
            message: data.message
        }, function () { window.location = "/" })
    }

    function onConnected(socket) {
        $("#connection-lost").addClass("hidden")
        me.socket.emit("join", { "session": sessionKey }, onJoinResponse)
    }

    function onDisconnected(socket) {
        $("#connection-lost").removeClass("hidden")
    }

    function onReconnected(socket) {
        $("#connection-lost").addClass("hidden")
    }

    function onJoinResponse(response) {
        if (response.success != true) {
            Alerts().alert({
                title: "Error",
                message:"You are not connected to the session" },
                function () { window.location = "/" })
        }
    }

    function connect(uri) {
        me.socket = io.connect(uri)

        me.socket.on("connect", onConnected)
        me.socket.on("disconnect", onDisconnected)
        me.socket.on("reconnect", onReconnected)
        me.socket.on("kick", onKick)
        me.socket.on("user", function(data) {
            me.user=data;
            me.users.update();
        })
        me.socket.on("stage", me.stage.processMessage)
        me.socket.on("chat", me.chat.processMessage)
        me.socket.on("users", function(data) {
            me.infoLine.setUsers(data)
            me.users.setUsers(data)
        })
        me.socket.on("quorum_change_code", me.quorum.showQuorumChangeCode)
        me.socket.on("timer", me.timer.processMessage)
    }

    me.emit = function(eventName, data, response) {
        if (!response) {
            me.socket.emit(eventName, data)
        } else {
            me.socket.emit(eventName, data, response)
        }
    }

    me.connect = connect

    return me
}


$(document).ready(function() {
    var host = "//" + document.domain + ":" + location.port
    var sessionKey = $("#session-key").text().trim()
    var sessionData = JSON.parse($("#session-data").text())
    var controller = createSessionController(sessionKey, sessionData)
    window.controller = controller

    controller.connect(host)

    $(".template").each(function (n) {
        var name = $(this).data("name")
        var html = $(this).html()
        Handlebars.registerPartial(name, html)
    })
})


/* File: ./een/web/blueprints/session/js/session_info_line.js */

/* Manages state of information line
 *
 * param session: session controller
 * param node: node to control
 */
function InfoLineController(session, node) {

    // sets end time of the session
    // param time: session end time
    function setEndTime(time) {
        endTime = time
    }

    // sets list of users online
    // param users: list of users
    function setUsers(list) {
        users = list
    }

    // sets title
    // param title: session title
    function setSessionTitle(title) {
        sessionTitle = title
    }

    // internal members

    var endTime = new Date()
    var sessionTitle = ""
    var users = []
    var template = Handlebars.compile("{{> info_line }}")
    var timer = setInterval(update, 1000)

    // renders info line
    function update() {
        var now = new Date()
        var td = timeDiff(now, endTime)
        var usersByRole = groupBy(users, "role")
        var fiveMinutes = 1000 * 60 * 5

        node.html(template({
            session: {title: sessionTitle},
            groups: usersByRole,
            users: users,
            time: td,
            style: td.negative ? "danger" : td.distance < fiveMinutes ? "warning" : "primary",
            overtime: td.negative
        }))

        node.removeClass("hidden")
    }

    return { setEndTime, setUsers, setSessionTitle }
}


/* File: ./een/web/blueprints/session/js/session_manage.js */

function createManageController(controller) {
    var nextStageLabel = $("#state-next")
    var alerts = Alerts()


    $(".change-stage").on("click", function(e) {
        e.preventDefault()
        var value = $(this).data("value")
        changeStage(value)
    })

    $(".run-close").on("click", function(e) {
        e.preventDefault()
        closeSession()
    })

    $("#stage").on("click", ".run-close", function(e) {
        e.preventDefault()
        closeSession()
    })

    $(".timer-set").on("click", function(e) {
        e.preventDefault()
        var minutes = $(this).data("value")
        if (minutes == "custom") {
            minutes = promptCustomTimer()
        } else {
            setCountdownTimer(minutes)
        }
    })

    $("#session-quorum-set").on("click", function(e) {
        e.preventDefault()
        controller.quorum.requestChange()
    })


    function onChangeStageResponse(data) {
        if (data.next.title != data.current.title) {
            var title = data.next.title ? " &laquo;" + data.next.title + "&raquo;" : ""
            nextStageLabel.html(title)
        } else {
            var type = data.next.type ? " (" + data.next.type + ")" : ""
            nextStageLabel.html(type)
        }
    }

    function onCloseSessionResponse(data) {
        alerts.alert({title: "Closed", message: "Session is closed. You will be redirected to the dashboard page."}, function () {
            window.location = "/account"
        })
    }

    // Actions ---------------------------------------------------------------------------------------------------------

    function changeStage(value) {
        controller.socket.emit("change_stage", { value: value }, onChangeStageResponse)
    }

    function closeSession() {
        controller.socket.emit("close", onCloseSessionResponse)
    }

    function setCountdownTimer(minutes) {
        controller.socket.emit("timer", { interval: minutes })
    }

    function promptCustomTimer() {
        $.confirm({
            theme: "bootstrap",
            title: 'Custom timer',
            content: $("#timer-custom").html(),
            buttons: {
                formSubmit: {
                    text: 'Submit',
                    btnClass: 'btn btn-primary',
                    action: function () {
                        var value = this.$content.find('#timer-custom-value').val()
                        if (!value) {
                            $.alert('Provide a valid value')
                            return false
                        }
                        setCountdownTimer(value)
                    }
                },
                cancel: {
                    btnClass: "btn btn-danger",
                    text: "Cancel",
                    action: function () {}
                }
            },
            onContentReady: function () {
                // bind to events
                var jc = this;
                this.$content.find('form').on('submit', function (e) {
                    // if the user submits the form by pressing enter in the field.
                    e.preventDefault();
                    jc.$$formSubmit.trigger('click'); // reference the button and click it
                })
            }
        })
    }


    return {}
}


/* File: ./een/web/blueprints/session/js/session_quorum.js */

/* Quorum controller. */
function QuorumController(session) {

    function requestChange() {
        showChangeQuorumDialog()
    }

    function showQuorumChangeCode(data) {
        alerts.alert({
            title: "Quorum Change Code",
            message: data.code
        })
    }

    // Private members

    var alerts = Alerts()

    function showChangeQuorumDialog() {
        alerts.input({
            title: "Change Quorum",
            placeholder: "New Quorum"},
            onChangeQuorumDialogValueEntered)
    }

    function sendQuorumChangeRequest(value) {
        session.emit(
            "manage_session",
            { command: "set_quorum", value: Number(value) },
            onQuorumChangeRequestResponse)
    }

    function sendQuorumChangeCodes(value) {
        session.emit(
            "manage_session",
            { command: "set_quorum", codes: value },
            onQuorumChangeCodesResponse
        )
    }

    // Handlers
    function onChangeQuorumDialogValueEntered(value) {
        if (!Number.isInteger(Number(value))) {
            alerts.alert({
                title: "Value is not valid",
                message: "Please provide positive integer value"
            })
        } else {
            sendQuorumChangeRequest(value)
        }
    }

    function onQuorumChangeRequestResponse(response) {
        if (!response.success) {
            alerts.alert({title: "Unable to change Quorum", message: response.message})
            return
        }

        var names = response.users.join(", ")
        alerts.input({
            title: "Change Quorum",
            message: "Waiting codes from: " + names,
            placeholder: "Each code on a new line"},
            onQuorumCodeEntered)
    }

    function onQuorumCodeEntered(value) {
        var codesArray = value
            .split(/\s+/g)  // split by whitespace
            .filter(Number) // get numbers only
            .map(function(x) { return Number(x) }) // convert to numbers
        sendQuorumChangeCodes(codesArray)
    }

    function onQuorumChangeCodesResponse(response) {
        if (response.success) {
            alerts.alert({title: "Change Quorum", message: response.message})
        } else {
            alerts.alert({title: "Change Quorum", message: response.message})
        }
    }

    return { requestChange, showQuorumChangeCode }
}

/* File: ./een/web/blueprints/session/js/session_stage.js */

/* Stage Controller
 *
 * param session: Session
 * param proposalNode: Node to render proposal
 * param widgetsNode: Node to render stage widgets */
function StageController(session, proposalNode, widgetsNode) {

    // Process incoming message from server
    // param data: data from server
    function processMessage(data) {
        var proposalId = data.proposal_id
        var stageType = data.stage.type
        var nextStage = getController(proposalId, stageType) // controller for next stage
        var isStageChanged = (nextStage != currentStage)
        var isProposalChanged = (proposalId != (currentStage && currentStage.view().proposal_id))

        if (nextStage) {
            // extend data with additional info
            Object.assign(data, {
                stageType: function() { return "stage_" + data.stage.type },
                proposal: data.proposal_id ? proposals[data.proposal_id] : null,
                user: session.user
            })

            // updates state of the stage controller
            if (nextStage.setState) {
                nextStage.setState(data)
            }

            if (isStageChanged) {
                onStageChanged(currentStage, nextStage)
            }

            if (isProposalChanged) {
                var proposal = data.proposal_id ? proposals[data.proposal_id] : null
                onProposalChanged(proposal)
            }
            currentStage = nextStage
        }

        // state is changes, so render it
        renderWidget()

        if (data.stage.type != "acquaintance") {
            $(".panel-body", proposalNode).addClass("proposal-block")
        } else {
            $(".panel-body", proposalNode).removeClass("proposal-block")
        }
    }

    function requestRender() {
        renderWidget()
    }

    // Private members

    // Renders current stage
    function renderWidget() {
        if (!currentStage) return;

        widgetsNode.html(widgetTemplate(currentStage.view()))
        if (currentStage.register) currentStage.register()
    }

    // Renders specified proposal
    function renderProposal(proposal) {
        var template = proposalTemplate(proposal)
        proposalNode.html(template)
    }

    // Event handlers

    function onStageChanged(current, next) {
        // stage changed - stop the timer
        session.timer.stop()

        // unregister handlers from current stage
        if (current && current.unregister) {
            currentStage.unregister()
        }

        // call "enter" handler for next stage
        if (next && next.enter) {
            nextStage.enter()
        }
    }

    function onProposalChanged(proposal) {
        renderProposal(proposal)
    }

    // Private members

    var currentStage = null
    var proposalTemplate = Handlebars.compile("{{> proposal}}")
    var widgetTemplate = Handlebars.compile("{{> stage_template }}")
    var proposals = JSON.parse($("#proposals").html())
    var controllers = {} // map of controllers keyed by proposalId

    // returns controllers for specified proposal
    // param proposalId: Id of proposal
    // param stage: Stage
    function getController(proposalId, stage) {
        var c = controllers[proposalId]
        if (!c) {
            c = createControllers()
            controllers[proposalId] = c
        }
        return c[stage]
    }

    // creates a bunch of controllers for each stage
    function createControllers() {
        return {
            "agenda": SimpleStageController(session),
            "acquaintance": AcquaintanceStageController(session),
            "closed": SimpleStageController(session),
            "voting": VotingStageController(session),
            "votingresults": VotingResultsStageController(session),
            "commenting": CommentingStageController(session),
            "discussion": DiscussionStageController(session)
        }
    }

    return { processMessage, requestRender }
}

/* File: ./een/web/blueprints/session/js/session_timer.js */

/* Manages the timer. */
function createTimerController(controller) {

    function processMessage(data) {
        var minutes = data.interval

        if (!minutes) {
            stop()
            return
        }

        var isAppendMode = minutes.toString().indexOf("+") != -1
        if (isAppendMode) { // append to current time
            if (end == null) end = new Date().getTime()
            end += minutes * 60000
        } else { // set new time
            end = new Date().getTime() + (minutes * 60000)
        }
        countdownTo(new Date(end))
    }

    function countdownTo(date) {
        // timer was started previously.
        // stop it before start new one
        if (timer) {
            clearInterval(timer)
        }

        // sets new timer
        end = date.getTime()
        timer = setInterval(render, 1000)

        showPanel(true)
        render()
    }

    function stop() {
        end = null
        if (timer) {
            clearInterval(timer)
        }
        showPanel(false)
    }

    function on(handler) {
        callbacks.push(handler)
    }

    function off(handler) {
        callbacks.remove(handler)
    }

    // Private members

    var timer = null  // timer object
    var end   = null  // countdown to this date/time
    var panel = $("#timer-panel") // timer's panel
    var callbacks = []

    // Shows timer's panel
    // param: value  - true/false
    // param: danger - true/false, highlight panel or not
    function showPanel(value, danger) {
        panel.toggle(value)
        if (danger) {
            panel.addClass("panel-danger")
        } else {
            panel.removeClass("panel-danger")
        }
    }

    // Renders panel
    function render() {
        var now = new Date().getTime()
        var distance = end - now
        for (c in callbacks) {
            callbacks[c](distance)
        }

        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
        var seconds = Math.floor((distance % (1000 * 60)) / 1000)

        minutes = String("00" + minutes).slice(-2)
        seconds = String("00" + seconds).slice(-2)

        // Display the result in the element with id="demo"
        document.getElementById("timer").innerHTML =
            hours ? hours + "h " + minutes + ":" + seconds :
                    minutes + ":" + seconds

        if (distance < 0) {
            clearInterval(timer)
            document.getElementById("timer").innerHTML = "00:00"
            end = null
        }

        if (distance < 1000 * 45) {
            showPanel(true, true)
        }
    }

    return { processMessage, countdownTo, stop, on, off }
}

/* File: ./een/web/blueprints/session/js/session_users.js */

/* Manages the list of connected users.
 *
 * param session: session controller
 * param container: container to display the list of users
 */
function UsersPanelController(session, container) {

    $(document).on("click", ".kick", onKickButtonClicked)

    // Updates panel
    function update() {
        render()
    }

    // Sets list of connected users
    // param data: array of connected users
    //             [{name: "akd", role: "secretary"}, ...]
    function setUsers(data) {
        users = data
        update()
    }


    // Private members

    var users    = []
    var template = Handlebars.compile("{{> user_line }}")
    var alerts   = Alerts()


    // On "kick" button clicked
    function onKickButtonClicked(e) {
        e.preventDefault()
        var userId = $(this).data("user-id")

        alerts.input({title: "Remove user from session", placeholder: "Reason"}, function(reason) {
            session.emit("kick", {user: userId, reason: reason || "No reason provided"})
        })
    }

    function render() {
        container.empty()
        for (user of users) {
            container.append(template(user, {data: {user: session.user}}))
        }
    }

    return { setUsers, update }
}


/* File: ./een/web/blueprints/session/js/stages/acquaintance_controller.js */

/* Acquaintance stage controller
 * Provides basic functionality
 * param session: session
 */
function AcquaintanceStageController(session) {

    function setState(value) {
        state = value

        // get unique roles
        roles = state.comments.list.map(function(obj) { return obj.role })
        roles = roles.filter(function(v, i) { return roles.indexOf(v) == i })
   }

    function register() {
        $(".selectpicker").selectpicker()
        $(".vote-details").popover({ trigger: "hover" })
    }

    function view() {
        return {
            comments: {
                comments: state.comments.list,
                roles: roles
            },
            voting: state.voting,
            stageType: state.stageType,
            proposal_id: state.proposal_id
        }
    }

    // Private members

    var state = null
    var roles = []

    return { view, setState, register }
}


/* File: ./een/web/blueprints/session/js/stages/commenting_controller.js */

function CommentingStageController(session) {
    var commentQuote = null
    var state = null
    var comments = []
    var filterCheckedTypes = ["plus", "minus", "info"]
    var filterCheckedRoles = null
    var filterCheckedSort = ["timestamp"]

    function register() {
        $("#comment-private").on("change", onPrivateCommentsCheckboxChanged)
        $(".comment-add").on("click", onAddCommentButtonClicked)
        $("#proposal-content").on("mouseup", onProposalContentMouseUp)

        $(".selectpicker").selectpicker()
        $("#comment-filter-type").on("changed.bs.select", onFilterChanged)
        $("#comment-filter-role").on("changed.bs.select", onFilterChanged)
        $("#comment-sort").on("changed.bs.select", onFilterChanged)

        $("#comment-print").on("click", onPrintClicked)
    }

    function setState(value) {
        state = value

        comments = state.comments.list
        roles = state.comments.list.map(function(obj) { return obj.role })
        roles = roles.filter(function(v, i) { return roles.indexOf(v) == i })
        filterCheckedRoles = roles
        updateComments()
    }

    function view() {
        var permissions = session.user.permissions

        return Object.assign({}, state, {
            showComments: !state.private || permissions.indexOf("comment.manage") != -1,
            showAddComment: permissions.indexOf("comment") != -1,
            showAddCommentLink: permissions.indexOf("comment") != -1 && !state.private,
            comments: {
                showFilter: true,
                showPrint: true,
                manageable: permissions.indexOf("comment.manage") != -1,
                privateCheckedState: state.private ? "checked" : "",
                comments: comments,
                roles: roles,
                filterTypeValue: function(name) { return filterCheckedTypes.indexOf(name) != -1 ? "selected" : "" },
                filterRoleValue: function(name) { return filterCheckedRoles.indexOf(name) != -1 ? "selected" : "" },
                filterSortValue: function(name) { return filterCheckedSort.indexOf(name) != -1 ? "selected" : "" }
            }
        })
    }

    // UI Event handlers

    // "Secret ballot" checkbox clicked
    function onPrivateCommentsCheckboxChanged(e) {
        var val = $(this).is(":checked") // is checked?
        setCommentingPrivacy(val)
    }

    // on any filter checkbox changed
    function onFilterChanged(e) {
        // get list of checked types and roles
        filterCheckedTypes = $("#comment-filter-type").val()
        filterCheckedRoles = $("#comment-filter-role").val()
        filterCheckedSort = $("#comment-sort").val()
        updateComments()
        session.stage.requestRender()
    }

    function onProposalContentMouseUp(e) {
        var selection = window.getSelection().toString()
        setCommentQuote(selection)
    }

    function onAddCommentButtonClicked(e) {
        e.preventDefault();
        var buttonClicked = $(this)
        var content = $("#comment-message").val()
        var type = $("#comment-type option:selected").val()
        comment(content, type, commentQuote)
    }

    function onCommentSubmittedResponse(data) {
        var flash = $("#comment-submitted")
        flash.removeClass("hidden")
        setTimeout(function() { flash.alert("close") }, 5000)
    }

    function onPrintClicked(e) {
        e.preventDefault()

        var alert = Alerts().alert({
            title:"Printing",
            message:"We are printing your document. Please wait a moment."
        })

        var commentsCriteria = { proposal_id: state.proposal_id, stage: state.comments.stage }
        var data = {type:"comments", "criteria": commentsCriteria}

        controller.emit("print", data, function(data) {
            if (data.success) {
                $.fileDownload("/files/" + data.path)
                alert.close()
            } else {
                Alerts().alert({title: "Error", message: data.message})
            }
        })
    }

    // Actions

    function comment(content, type, quote) {
        session.socket.emit("comment", {content, type, quote}, onCommentSubmittedResponse)
    }

    function setCommentingPrivacy(value) {
        session.socket.emit("manage", {private: value})
    }

    function updateComments() {
        showComments(function(x) {
            return filterCheckedTypes.indexOf(x.type) >= 0 &&
                filterCheckedRoles.indexOf(x.role) >= 0
        }, function (a, b) {
            if (filterCheckedSort != "time") {
                var fa = a[filterCheckedSort]
                var fb = b[filterCheckedSort]
                return fa !== fb ? fa < fb ? -1 : 1 : 0
            } else {
                var fa = Date.parse(a[filterCheckedSort])
                var fb = Date.parse(b[filterCheckedSort])
                return fa !== fb ? fa < fb ? -1 : 1 : 0
            }
        })
    }

    function showComments(func, sort) {
        for (c of comments) {
            c.visible = func(c)
        }
        if (sort) {
            comments = comments.sort(sort)
        }
    }

    function setCommentQuote(value) {
        commentQuote = value
        $("#quotation").html(commentQuote)
        $("#quotation").attr("hidden", value ? null : "hidden")
    }

    return { register, view, setState }
}


/* File: ./een/web/blueprints/session/js/stages/discussion_controller.js */

function DiscussionStageController(controller) {
    var state

    function register() {
        $("#discussion-accept").on("change", onAcceptCheckboxChanged)
        $(".discussion-give-voice").on("click", onGiveVoiceToUserClicked)
        $(".discussion-remove").on("click", onRemoveUserFromQueueClicked)
        $("#discussion-raise-hand").on("click", onRaiseHandButtonClicked)
        $("#discussion-withdraw-hand").on("click", onWithdrawHandButtonClicked)
        $("[data-toggle='tooltip']").tooltip()
    }

    function setState(value) {
        state = value
    }

    function view() {
        return state
    }

    function onAcceptCheckboxChanged(e) {
        var value = $(this).is(":checked")
        acceptApplications(value)
    }

    function onGiveVoiceToUserClicked(e) {
        e.preventDefault()
        var userId = $(this).data("user-id")
        giveVoice(userId)
    }

    function onRemoveUserFromQueueClicked(e) {
        e.preventDefault()
        var userId = $(this).data("user-id")
        remove(userId)
    }

    function onRaiseHandButtonClicked(e) {
        e.preventDefault()
        raiseHand()
    }

    function onWithdrawHandButtonClicked(e) {
        e.preventDefault()
        withdrawHand()
    }

    // Actions

    function acceptApplications(value) {
        controller.socket.emit("manage", {command: "accept", value: value})
    }

    function giveVoice(userId) {
        controller.socket.emit("manage", {command: "give_voice", user_id: userId})
    }

    function remove(userId) {
        controller.socket.emit("manage", {command: "remove", user_id: userId})
    }

    function raiseHand() {
        controller.socket.emit("manage", { command: "raise_hand" })
    }

    function withdrawHand() {
        controller.socket.emit("manage", { command: "withdraw_hand" })
    }

    return { register, view, setState }
}


/* File: ./een/web/blueprints/session/js/stages/simple_controller.js */

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


/* File: ./een/web/blueprints/session/js/stages/voting_controller.js */

/* Voting Stage Controller
 *
 * param session: session
 */
function VotingStageController(session) {

    function setState(value) {
        state = value
    }

    function register() {
        $("#vote-private").on("change", onSecretBallotCheckboxChanged)
        $(".vote").on("click", onVoteButtonClicked)
        $(".selectpicker").selectpicker({
            style: 'btn-info btn-xs',
            size: 4, width: "100px"
        })
        $("#vote-threshold").on("changed.bs.select", onVoteThresholdChanged)
        session.timer.on(onTimerTick)
    }

    function unregister() {
        session.timer.off(onTimerTick)
    }

    function view() {
        var permissions = session.user.permissions

        return Object.assign(state, {
            voteStatus: voteStatus, timeIsOver,
            quorum: state.quorum,
            isFinalVote: state.type == "final",
            isVoteSubmitted: voteStatus.success == true,
            isVoteNotAccepted: voteStatus.success == false,
            isVoteChanged: voteStatus.prev && voteStatus.prev != voteStatus.value,
            vote: voteViewName(voteStatus.value),
            prevVote: voteViewName(voteStatus.prev),
            canVote: !timeIsOver && permissions.indexOf("vote") != -1,
            canManage: permissions.indexOf("vote.manage") != -1,
            privateChecked: state.private ? "checked" : "",
            showPrivateAlert: state.private && permissions.indexOf("vote") != -1,
            noQuorum: state.type == "final" && state.can_vote < state.quorum,
            threshold: state.threshold,
            selectedThreshold: function(val) { return val == state.threshold ? "selected" : ""}
        })
    }

    // Private members

    var state = null
    var voteStatus = {success:undefined, prev:undefined, value:undefined} // user's vote status
    var timeIsOver = false

    // handlers

    function onSecretBallotCheckboxChanged(e) {
        var val = $(this).is(":checked") // is checked?
        setVotingPrivacy(val)
    }

    function onVoteButtonClicked(e) {
        e.preventDefault()
        var value = $(this).data("vote")
        vote(value)
    }

    function onVoteResponse(response) {
        voteStatus = response
        session.stage.requestRender()
    }

    function onTimerTick(value) {
        if (value <= 0 && !timeIsOver) {
            timeIsOver = true
            session.stage.requestRender()
        } else if (value > 0 && timeIsOver) {
            timeIsOver = false
            session.stage.requestRender()
        }
    }

    function onVoteThresholdChanged(e) {
        var threshold = $(e.currentTarget).val()
        setVotingThreshold(threshold)
    }

    // Actions

    function vote(value) {
        session.emit("vote", {value: value}, onVoteResponse)
    }

    function setVotingPrivacy(value) {
        session.emit("manage", {cmd: "set_private", value: value})
    }

    function setVotingThreshold(value) {
        session.emit("manage", {cmd: "set_threshold", value: value})
    }

    function voteViewName(value) {
        if (value == "yes") return "In Favor"
        if (value == "no") return "Against"
        if (value == "undecided") return "Abstention"
        return value
    }

    return { register, unregister, view, setState }
}

/* File: ./een/web/blueprints/session/js/stages/voting_results_controller.js */

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
