/**
 * Contains functions for Web Publisher 2.0
 *
 * @author Siri Chongasamethaworn (siri_c@nomagicasia.com)
 * @version 1.1 March 17, 2008
 */
var usecontextmenu = false;
var nonamedNode = '< >';
var nonamedLink = '';
var gotoElementId = '';
var resourcesLocation = contextPath;
if (resourcesLocation != '' && !/\/$/.test(resourcesLocation)) 
    resourcesLocation = resourcesLocation + '/';
Library.load({
    'js/animate.js': ['Graphics', 'Content']
});
Library.load({
    'js/cookies.js': ['Cookies']
});
Library.load({
    'js/map.js': ['Map']
});
Content.imgShow = resourcesLocation + 'images/down_triangle.gif';
Content.imgHide = resourcesLocation + 'images/right_triangle.gif';
addEvent(window, 'load', repaint);
addEvent(window, 'load', initWeb);
addEvent(window, 'resize', function(){
    resize();
});
var tree;
var viewbar;
var actionbar;
var currentPageId;

var backStack = new Stack();
var forwardStack = new Stack();

var documentMap = new Map();

var documentation;
var firstShow;
var evt;

function resize(){
    var splitpane = document.getElementById('splitpane');
    splitPane.repaint();
}

function repaint(){
    var divs = document.getElementsByTagName('div');
    for (var i = 0; i < divs.length; i++) {
        var className = divs[i].className + ' ';
        if (className.indexOf("thead") != -1) {
            var headerText = divs[i].innerHTML;
            var contentNode = nextSibling(divs[i]);
            if (divs[i].hasChildNodes() && contentNode.id) {
                if (divs[i].childNodes[0].nodeName != 'IMG') {
                    var img = document.createElement('img');
                    img.src = Content.imgShow;
                    img.alt = '';
                    img.style.margin = '.1em';
                    img.contentId = contentNode.id;
                    img.onclick = function(){
                        Content.showHide(this, this.contentId);
                    };
                    divs[i].insertBefore(img, divs[i].childNodes[0]);
                }
            }
        }
    }
    splitPane.repaint();
}

function initWeb(){
    var nav = new Navigator();
    nav.menuLeftImg = 'url(' + resourcesLocation + 'images/navigator/containment_left.gif)';
    nav.menuLeftOverImg = 'url(' + resourcesLocation + 'images/navigator/containment_left_over.gif)';
    nav.menuRightImg = 'url(' + resourcesLocation + 'images/navigator/containment_right.gif)';
    nav.menuRightOverImg = 'url(' + resourcesLocation + 'images/navigator/containment_right_over.gif)';
    nav.repaint();
    var splitpane = document.getElementById('splitpane');
    if (splitpane) {
        var containmentButton = nav.getMenuLeftIcon();
        containmentButton.id = 'containmentButton';
        var cell = splitpane.rows[0].insertCell(0);
        cell.id = 'menupane';
        cell.style.verticalAlign = 'top';
        cell.appendChild(containmentButton);
        var containmentButtonWidth = ((containmentButton.offsetWidth / splitpane.offsetWidth) * 100);
        cell.style.width = containmentButtonWidth + '%';
    }
    var browser = document.getElementById('browser');
    if (browser) {
        var bar = document.createElement('div');
        bar.className = 'browserbar';
        if (browser.hasChildNodes()) 
            browser.insertBefore(bar, browser.childNodes[0]);
        else 
            browser.appendChild(bar);
        bar.appendChild(nav.getUnDockIcon());
        bar.appendChild(nav.getMinimizeIcon());
        bar.appendChild(document.createTextNode('Containment'));
    }
    var titlebar = document.getElementById('titlebar');
    var content = document.getElementById('splitpane-second');
    if (content != null && titlebar != null) {
        if (document.documentElement.clientHeight) 
            content.style.height = document.documentElement.clientHeight - titlebar.offsetHeight + 'px';
        else 
            content.style.height = window.innerHeight - titlebar.offsetHeight + 'px';
    }
    if (Cookies.getCookie('Navigator.pin') == 'false') 
        nav.togglePin(false);
}

function isHiddenNode(node){
    if (node.nodeType == 1) {
        // do not display hidden element
        var isHidden = node.getAttribute('isHidden');
        if (isHidden == 'true') 
            return true;
        return false;
    }
    return true;
}

function buildTree(li){
    var model = li.data;
    if (model == null) 
        return;
    var childNodes = model.childNodes;
    for (var c = 0; c < childNodes.length; c++) {
        if (childNodes[c].tagName == 'ownedElement') {
            var members = childNodes[c].childNodes;
            for (var m = 0; m < members.length; m++) {
                if (isHiddenNode(members[m])) 
                    continue;
                var emptyUL = document.createElement('ul');
                emptyUL.onExpand = function(){
                    var node = this.parentNode;
                    if (this.hasChildNodes()) {
                        return;
                    }
                    var childNodes = node.data.childNodes;
                    for (var c = 0; c < childNodes.length; c++) {
                        if (childNodes[c].tagName == 'ownedElement') {
                            var groupMap = new Array();
                            var members = childNodes[c].childNodes;
                            for (var p = 0; p < members.length; p++) {
                                if (members[p].nodeType == 1) {
                                    if (isHiddenNode(members[p]) || members[p].tagName == 'diagram') 
                                        continue;
                                    // display element, icon
                                    var icon = members[p].getAttribute('icon');
                                    var childNode = null;
                                    // group relationship
                                    if (members[p].getAttribute('isRelationship') == 'true') {
                                        var relationUL;
                                        if (this.firstChild && this.firstChild.elementName == 'Relations') 
                                            relationUL = this.firstChild.lastChild;
                                        else {
                                            var relationLI = addNode(this, 'Relations', 'javascript:void(0);', 'zesapelem_files/icon_22154688.jpg');
                                            relationLI.setAttribute('refid', 'relations');
                                            relationUL = document.createElement('ul');
                                            relationUL.onExpand = function(){
                                            };
                                            relationUL.onCollapse = function(){
                                            };
                                            relationLI.appendChild(relationUL);
                                            if (this.firstChild) 
                                                this.insertBefore(relationLI, this.firstChild);
                                            else 
                                                this.appendChild(relationLI);
                                            tree.renderNode(relationLI);
                                        }
                                        var name = members[p].getAttribute('humanType');
                                        if (members[p].getAttribute('name')) 
                                            name += ':' + members[p].getAttribute('name');
                                        childNode = addNode(relationUL, name, "javascript: gotoElement('" + members[p].getAttribute('refid') + "');", icon);
                                        childNode.data = members[p];
                                        childNode.setAttribute('refid', members[p].getAttribute('refid'));
                                    }
                                    else {
                                        var groupBy = members[p].getAttribute('groupBy');
                                        if (groupBy) {
                                            if (!groupMap[groupBy]) 
                                                groupMap[groupBy] = new Array();
                                            groupMap[groupBy][groupMap[groupBy].length] = members[p];
                                        }
                                        else {
                                            var name;
                                            if (members[p].getAttribute('represents')) 
                                                name = members[p].getAttribute('represents');
                                            else if (members[p].getAttribute('name')) 
                                                name = members[p].getAttribute('name');
                                            else 
                                                name = nonamedNode || nonamedNode == '' ? nonamedNode : members[p].getAttribute('humanType');
                                            childNode = addNode(this, name, "javascript: gotoElement('" + members[p].getAttribute('refid') + "');", icon);
                                            childNode.data = members[p];
                                            childNode.setAttribute('refid', members[p].getAttribute('refid'));
                                            if (groupMap) {
                                                var childGroup = groupMap[childNode.getAttribute('refid')];
                                                if (childGroup) {
                                                    var tmpOwnedElement;
                                                    var tmpChildNodes = childNode.data.childNodes;
                                                    for (var tmp = 0; tmp < tmpChildNodes.length; tmp++) {
                                                        if (tmpChildNodes[tmp].tagName == 'ownedElement') {
                                                            tmpOwnedElement = tmpChildNodes[tmp];
                                                            break;
                                                        }
                                                    }
                                                    if (typeof(tmpOwnedElement) == 'undefined') {
                                                        tmpOwnedElement = createElement('ownedElement');
                                                        childNode.data.appendChild(tmpOwnedElement);
                                                    }
                                                    if (tmpOwnedElement) {
                                                        for (var g = 0; g < childGroup.length; g++) {
                                                            childGroup[g].removeAttribute('groupBy');
                                                            tmpOwnedElement.appendChild(childGroup[g]);
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    if (childNode != null) 
                                        buildTree(childNode);
                                }
                            }
                        }
                        else 
                            if (childNodes[c].tagName == 'ownedDiagram') {
                                var members = childNodes[c].childNodes;
                                for (var m = 0; m < members.length; m++) {
                                    if (members[m].nodeType == 1) {
                                        var icon = members[m].getAttribute('icon');
                                        var name;
                                        if (members[m].getAttribute('name')) 
                                            name = members[m].getAttribute('name');
                                        else 
                                            name = nonamedNode || nonamedNode == '' ? nonamedNode : members[m].getAttribute('humanType');
                                        var childNode = addNode(this, name, "javascript: gotoElement('" + members[m].getAttribute('refid') + "');", icon);
                                        childNode.data = members[m];
                                        childNode.setAttribute('refid', members[m].getAttribute('refid'));
                                        // comment below and uncomment buildTree(childNode) to see diagram inner node
                                        tree.renderNode(childNode);
                                    // buildTree(childNode);
                                    }
                                }
                            }
                    }
                };
                emptyUL.onCollapse = function(){
                    splitPane.repaint();
                };
                li.appendChild(emptyUL);
                break;
            }
        }
    }
    tree.renderNode(li);
}

/**
 * Search and return tree node from refid
 * @param refid refid
 * @return LI tree node
 */
function findNode(refid){
    var searchResults = new Array(0);
    var dataModel = tree.root.firstChild.data;
    var regx = new RegExp(refid, 'i');
    match(dataModel, 'refid', regx, searchResults);
    if (searchResults.length == 1) {
        var parentNode = searchResults[0];
        var nodePath = new Array();
        while (parentNode && parentNode.tagName != 'magicdraw') {
            if (parentNode.nodeType == 1) {
                var refid = parentNode.getAttribute('refid');
                if (refid) 
                    nodePath[nodePath.length] = refid;
                parentNode = parentNode.parentNode;
            }
        }
        var rootTree = document.getElementById(tree.treeId);
        expandPath(nodePath);
        searchResults = new Array(0);
        match(rootTree, 'refid', regx, searchResults);
        return searchResults[0];
    }
    return null;
}

/**
 * Select node on containment tree
 * @param node LI or A element of tree node
 */
function selectNode(node){
    if (node) {
        if (node.tagName == 'LI') {
            var childNodes = node.childNodes;
            for (var i = 0; i < childNodes.length; i++) {
                if (childNodes[i].name == 'anchorNode') {
                    var root = document.getElementById(tree.treeId);
                    var nodes = root.getElementsByTagName('li');
                    for (var n = 0; n < nodes.length; n++) {
                        var anchorNodes = nodes[n].childNodes;
                        for (var a = 0; a < anchorNodes.length; a++) {
                            if (anchorNodes[a].name == 'anchorNode') 
                                anchorNodes[a].style.backgroundColor = '';
                        }
                    }
                    childNodes[i].style.backgroundColor = '#99CCFF';
                }
            }
        }
        else 
            if (node.tagName == 'A') {
                if (node.name == 'anchorNode') {
                    var root = document.getElementById(tree.treeId);
                    var nodes = root.getElementsByTagName('li');
                    for (var n = 0; n < nodes.length; n++) {
                        var anchorNodes = nodes[n].childNodes;
                        for (var a = 0; a < anchorNodes.length; a++) {
                            if (anchorNodes[a].name == 'anchorNode') 
                                anchorNodes[a].style.backgroundColor = '';
                        }
                    }
                    node.style.backgroundColor = '#99CCFF';
                }
            }
    }
}

function addNode(ul, nodeName, href, icon){
    var node = document.createElement('li');
    node.elementName = nodeName;
    var anchor = document.createElement('a');
    anchor.appendChild(document.createTextNode(nodeName));
    anchor.name = 'anchorNode';
    anchor.href = href;
    anchor.style.verticalAlign = 'middle';
    anchor.style.marginLeft = '4px';
    anchor.style.marginRight = '4px';
    anchor.onclick = function(){
        selectNode(this);
    };
    node.appendChild(anchor);
    if (icon) {
        var imgAnchor = document.createElement('a');
        imgAnchor.href = href;
        imgAnchor.style.verticalAlign = 'middle';
        imgAnchor.onclick = anchor.onclick;
        var img = document.createElement('img');
        img.src = icon;
        img.alt = '';
        img.border = '0';
        img.height = '16';
        img.width = '16';
        img.style.verticalAlign = 'middle';
        imgAnchor.appendChild(img);
        node.insertBefore(imgAnchor, anchor);
    }
    ul.appendChild(node);
    return node;
}

/**
 * Shortcut to create HTML element with link
 * @param parentNode link container
 * @param linkToElement DOM element
 */
function createLink(parentNode, linkToElement){
    var refid = linkToElement.getAttribute('refid');
    var name = linkToElement.getAttribute('name');
    var icon = linkToElement.getAttribute('icon');
    
    firstShow = false;
    
    if (icon) {
        var fieldAnchor = document.createElement('a');
        fieldAnchor.href = "javascript: showSpec('" + refid + "');";
        var fieldImage = document.createElement('img');
        fieldImage.alt = '';
        fieldImage.border = '0';
        fieldImage.height = '16';
        fieldImage.width = '16';
        fieldImage.src = icon;
        fieldAnchor.appendChild(fieldImage);
        parentNode.appendChild(fieldAnchor);
    }
    if (!name) 
        name = nonamedLink || nonamedLink == '' ? nonamedLink : linkToElement.tagName;
    if (refid && name != '') {
        var fieldAnchor = document.createElement('a');
        fieldAnchor.href = "javascript: showSpec('" + refid + "');";
        fieldAnchor.style.marginLeft = '4px';
        fieldAnchor.style.marginRight = '4px';
        fieldAnchor.appendChild(document.createTextNode(name));
        fieldAnchor.onmouseover = function(e){
            evt = e ? e : event;
            var target = evt.target ? evt.target : evt.srcElement;
            documentation = null;
            if (documentMap.containsKey(refid)) {
                documentation = documentMap.get(refid);
                createDocBallon();
            }
            else {
                XMLRequest.send(resourcesLocation + '/xml/' + refid + '.xml', function(responseXML){
                    if (responseXML) {
                        documentation = responseXML.getElementsByTagName('documentation').item(0);
                        if (documentation != null) {
                            documentMap.put(refid, documentation);
                        }
                        createDocBallon();
                    }
                }, false, true);
            }
        };
        fieldAnchor.onmouseout = function(e){
            var value = document.getElementById('docBalloon');
            if (value) 
                value.style.visibility = 'hidden';
        };
        fieldAnchor.onclick = function(e){
            var value = document.getElementById('docBalloon');
            if (value) 
                value.style.visibility = 'hidden';
        };
        parentNode.appendChild(fieldAnchor);
    }
    else {
        parentNode.appendChild(document.createTextNode(name));
    }
    var additionalText = linkToElement.getAttribute('text');
    if (additionalText) {
        var cite = document.createElement('cite');
        cite.style.marginLeft = '4px';
        cite.style.marginRight = '4px';
        renderValueText(cite, additionalText);
        parentNode.appendChild(cite);
    }
}

function createDocBallon(){
    if (documentMap.size() == 50) {
        documentMap.remove(0);
    }
    
    if (documentation != null) {
        var value = document.getElementById('docBalloon');
        if (value == null) {
            var value = document.createElement('span');
            value.id = 'docBalloon';
            value.style.position = 'absolute';
            value.style.border = '#A5CFE9 solid 1px';
            value.style.fontFamily = 'arial';
            value.style.fontSize = 'x-small';
            value.style.padding = '3px';
            value.style.color = '#1B4966';
            value.style.background = '#FFFFFF';
            value.style.textAlign = 'left';
            value.style.zIndex = 900;
            value.onmouseout = function(e){
                var value = document.getElementById('docBalloon');
                if (value) 
                    value.style.visibility = 'hidden';
            };
            document.body.appendChild(value);
        }
        if (value.style.visibility == 'hidden' || !firstShow) {
            firstShow = true;
            var mic = Graphics.mousePosition(evt);
            var mouseX = mic.x + 2;
            var mouseY = mic.y + 2;
            value.style.left = mouseX + 'px';
            value.style.top = mouseY + 'px';
            value.style.visibility = 'visible';
            removeAll(value);
            renderValueNode(value, documentation);
        }
    }
}

function selectView(view){
    viewbar.currentView = view;
    var viewtab = document.getElementById('viewtab');
    var sib = firstChild(viewtab);
    while (sib != null) {
        sib.className = '';
        if (sib.tabName == view) {
            sib.className = 'active';
            sib.style.display = 'block';
        }
        sib = nextSibling(sib);
    }
    var modeItem = document.getElementById('modeItem');
    if (view == 'specification') 
        modeItem.setEnabled(true);
    else 
        modeItem.setEnabled(false);
}

function createViewBar(model){
    if (viewbar) 
        return viewbar;
    // lazy initialize
    viewbar = document.createElement('div');
    viewbar.id = 'viewbar';
    viewbar.currentType = model.tagName == 'diagram' ? 'diagram' : 'element';
    viewbar.currentView = 'specification';
    // tab bar
    var tabul = document.createElement('ul');
    tabul.id = 'viewtab';
    tabul.className = 'tab';
    var diali = document.createElement('li');
    diali.id = 'diagramtab';
    diali.tabName = 'diagram';
    diali.appendChild(document.createTextNode('Diagram'));
    diali.onclick = function(){
        selectView(this.tabName);
        var content = document.getElementById('content');
        renderDiagram(content.model, content.diagamModel);
        repaint();
    };
    tabul.appendChild(diali);
    var speli = document.createElement('li');
    speli.id = 'specificationtab';
    speli.tabName = 'specification';
    speli.appendChild(document.createTextNode('Specification'));
    speli.onclick = function(){
        selectView(this.tabName);
        var content = document.getElementById('content');
        renderElement(content.model);
        repaint();
    };
    tabul.appendChild(speli);
    viewbar.appendChild(tabul);
    
    // view mode
    var content = document.getElementById('content');
    if (typeof(content.mode) == 'undefined') 
        content.mode = 'standard';
    var modeItem = document.createElement('li');
    modeItem.id = 'modeItem';
    modeItem.style.cssFloat = 'right';
    modeItem.style.styleFloat = 'right';
    modeItem.style.margin = '0';
    modeItem.style.padding = '2px .5em 0 .5em';
    modeItem.style.cursor = 'default';
    modeItem.setEnabled = function(enabled){
        var childNodes = this.childNodes;
        for (var c = 0; c < childNodes.length; c++) 
            childNodes[c].disabled = !enabled;
    };
    // mode label
    var modeLabel = document.createElement('div');
    modeLabel.title = 'Display properties by selected filter';
    modeLabel.className = 'item';
    modeLabel.style.cssFloat = 'left';
    modeLabel.style.styleFloat = 'left';
    modeLabel.appendChild(document.createTextNode('Mode : '));
    modeItem.appendChild(modeLabel);
    // move options
    var modeSelect = document.createElement('select');
    modeSelect.id = 'modeSelect';
    modeSelect.onchange = function(){
        var content = document.getElementById('content');
        content.mode = this.options[this.selectedIndex].value;
        if (content.model) 
            renderElement(content.model);
        repaint();
    };
    var standardModeOption = document.createElement('option');
    standardModeOption.value = 'standard';
    if (content.mode == 'standard') 
        standardModeOption.selected = 'true';
    standardModeOption.appendChild(document.createTextNode('Standard'));
    modeSelect.appendChild(standardModeOption);
    var expertModeOption = document.createElement('option');
    expertModeOption.value = 'expert';
    if (content.mode == 'expert') 
        expertModeOption.selected = 'true';
    expertModeOption.appendChild(document.createTextNode('Expert'));
    modeSelect.appendChild(expertModeOption);
    var allModeOption = document.createElement('option');
    allModeOption.value = '';
    if (content.mode == '') 
        allModeOption.selected = 'true';
    allModeOption.appendChild(document.createTextNode('All'));
    modeSelect.appendChild(allModeOption);
    modeItem.appendChild(modeSelect);
    tabul.appendChild(modeItem);
    return viewbar;
}

function createActionBar(){
    if (actionbar) 
        return actionbar;
    // lazy initialize
    actionbar = document.createElement('div');
    actionbar.id = 'actionbar';
    var backButton = document.createElement('div');
    backButton.id = 'backButton';
    backButton.className = 'backDisabled';
    backButton.title = 'Back';
    backButton.onclick = function(){
        back();
    };
    actionbar.appendChild(backButton);
    var forwardButton = document.createElement('div');
    forwardButton.id = 'forwardButton';
    forwardButton.className = 'forwardDisabled';
    forwardButton.title = 'Forward';
    forwardButton.onclick = function(){
        forward();
    };
    actionbar.appendChild(forwardButton);
    var selectTreeButton = document.createElement('div');
    selectTreeButton.id = 'selectTreeButton';
    selectTreeButton.className = 'selectTreeButton';
    selectTreeButton.title = 'Select in Containment Tree';
    selectTreeButton.onclick = function(){
        var content = document.getElementById('content');
        if (content.model) {
            var node = findNode(content.model.getAttribute('id'));
            if (node) 
                selectNode(node);
            else 
                alert('Selected node is not appearing in containment tree');
        }
    };
    actionbar.appendChild(selectTreeButton);
    return actionbar;
}

/**
 * Value node renderer
 * @param value a HTML element containing value
 * @param element DOM element
 */
function renderValueNode(value, element){
    var text = nodeValue(element);
    renderValueText(value, text);
}

/**
 * Value text renderer
 * @param value a HTML element containing value
 * @param text text to display
 */
function renderValueText(value, text){
    if (text && text.indexOf('<html>') >= 0) {
        var startBodyIndex = text.indexOf('<body>');
        var endBodyIndex = text.indexOf('</body>', startBodyIndex);
        if (startBodyIndex > 0 && endBodyIndex > 0) {
            var htmlContent = text.substring(startBodyIndex, endBodyIndex);
            if (htmlContent.indexOf('mdel://') >= 0) {
                var reg = new RegExp('(<\s*a.+)href\s*=\s*\"(mdel://)(.*)\"(.*>)', 'gi');
                htmlContent = htmlContent.replace(reg, "$1href=\"javascript:showSpec('$3')\"$4");
            }
            value.innerHTML += htmlContent;
        }
    }
    else {
        var tokens = ('\u00A0' + text).split(/(\r\n)|\r|\n/);
        if (tokens.length > 1) {
            for (var t = 0; t < tokens.length; t++) {
                renderValueLink(value, tokens[t]);
                value.appendChild(document.createElement('br'));
            }
        }
        else {
            renderValueLink(value, tokens[0]);
        }
    }
}

/**
 * Value link renderer
 * @param value a HTML element containing value
 * @param text text containing link
 */
function renderValueLink(value, text){
    if (text == null) 
        text = '';
    if (text.indexOf('http://') == 1) {
        text = text.substring(1);
        var anchor = document.createElement('a');
        anchor.href = text;
        anchor.target = '_blank';
        anchor.appendChild(document.createTextNode(text));
        value.appendChild(anchor);
    }
    else 
        if (text.indexOf('file://') == 1) {
            var url = trim(text).substring(7);
            if (url.charAt(0) == '/') 
                url = url.substring(1);
            if (url.length >= 4) {
                var endsWith = url.substring(url.length - 4).toLowerCase();
                if (endsWith == '.flv' || endsWith == '.mp4') {
                    var container = document.createElement('div');
                    container.style.height = '344px';
                    container.style.width = '480px';
                    var embed = document.createElement('embed');
                    embed.src = resourcesLocation + 'swf/WebVideo.swf';
                    embed.type = 'application/x-shockwave-flash';
                    embed.width = '100%';
                    embed.height = '100%';
                    embed.setAttribute('flashvars', 'url=../../' + url);
                    embed.setAttribute('quality', 'high');
                    container.appendChild(embed);
                    value.appendChild(container);
                }
                else 
                    if (endsWith == '.mp3') {
                        var container = document.createElement('div');
                        container.style.height = '24px';
                        container.style.width = '320px';
                        var embed = document.createElement('embed');
                        embed.src = resourcesLocation + 'swf/WebAudio.swf';
                        embed.type = 'application/x-shockwave-flash';
                        embed.width = '100%';
                        embed.height = '100%';
                        embed.setAttribute('flashvars', 'url=' + url);
                        embed.setAttribute('quality', 'high');
                        value.appendChild(embed);
                        container.appendChild(embed);
                        value.appendChild(container);
                    }
                    else 
                        if (endsWith == '.swf') {
                            var container = document.createElement('div');
                            container.style.height = '344px';
                            container.style.width = '480px';
                            var embed = document.createElement('embed');
                            embed.src = url;
                            embed.type = 'application/x-shockwave-flash';
                            embed.width = '100%';
                            embed.height = '100%';
                            embed.setAttribute('quality', 'high');
                            container.appendChild(embed);
                            value.appendChild(container);
                        }
                        else {
                            var pathOffset = url.lastIndexOf('/');
                            var name = url;
                            if (pathOffset >= 0) 
                                name = url.substring(pathOffset + 1);
                            var anchor = document.createElement('a');
                            anchor.href = url;
                            anchor.target = '_blank';
                            anchor.appendChild(document.createTextNode(name));
                            value.appendChild(anchor);
                        }
            }
        }
        else {
            value.appendChild(document.createTextNode(text));
        }
}

/**
 * Render browser tree
 * @param responseXML a xml
 */
function renderBrowser(responseXML){
    var magicdraw;
    if (responseXML) 
        magicdraw = responseXML.getElementsByTagName('magicdraw')[0];
    if (magicdraw != null) {
        showLoading();
        var root = document.createElement('ul');
        root.id = 'tree';
        tree = new Tree(root.id);
        tree.image.plus = resourcesLocation + 'images/tree/plus.gif';
        tree.image.minus = resourcesLocation + 'images/tree/minus.gif';
        tree.root = root;
        var dataModel = firstChild(magicdraw);
        var node = addNode(root, dataModel.getAttribute('name'), "javascript: showSpec('" + dataModel.getAttribute('refid') + "');", dataModel.getAttribute('icon'));
        node.data = dataModel;
        node.setAttribute('refid', dataModel.getAttribute('refid'));
        buildTree(node);
        var browser = document.getElementById('browser');
        browser.appendChild(root);
        tree.expand(node);
        hideLoading();
        if (gotoElementId != '') {
            showSpec(gotoElementId, false);
        }
    }
}

var usehyperlink = false;
var useStack = false;
/**
 * Render model
 * @param responseXML a xml
 */
function renderModel(responseXML){
    var contextMenu = document.getElementById('elementcontextmenu');
    if (contextMenu) {
        contextMenu.style.disply = 'none';
        contextMenu.style.visibility = 'hidden';
        Shadow.removeShadow(contextMenu);
    }
    var magicdraw;
    if (responseXML) 
        magicdraw = responseXML.getElementsByTagName('magicdraw')[0];
    if (magicdraw == null) {
        alert('This element was not generated from project.');
        return;
    }
    var model = firstChild(magicdraw);
    // validate hyperlinkModelActive
    var stopRender = false;
    if (model.hasChildNodes && usehyperlink) {
        var childNodes = model.childNodes;
        for (var c = 0; c < childNodes.length && !stopRender; c++) {
            // Stereotype
            if (childNodes[c].tagName == 'appliedStereotype') {
                if (childNodes[c].hasChildNodes) {
                    var stereotypes = childNodes[c].childNodes;
                    for (var s = 0; s < stereotypes.length && !stopRender; s++) {
                        var stereotypeName = stereotypes[s].getAttribute('name');
                        if (stereotypeName == 'HyperlinkOwner') {
                            if (stereotypes[s].hasChildNodes) {
                                var properties = stereotypes[s].childNodes;
                                for (var p = 0; p < properties.length && !stopRender; p++) {
                                    var propertyName = properties[p].getAttribute('name');
                                    if (propertyName == 'hyperlinkModelActive') {
                                        if (properties[p].hasChildNodes) {
                                            var elements = properties[p].childNodes;
                                            for (var e = 0; e < elements.length && !stopRender; e++) {
                                                var refid = elements[e].getAttribute('refid');
                                                if (refid) {
                                                    usehyperlink = false;
                                                    gotoElement(refid);
                                                    stopRender = true;
                                                }
                                            }
                                        }
                                    }
                                    else if (propertyName == 'hyperlinkTextActive') {
                                            if (properties[p].hasChildNodes) {
                                                var elements = properties[p].childNodes;
                                                for (var e = 0; e < elements.length && !stopRender; e++) {
                                                    var uri = nodeValue(elements[e]);
                                                    var refid = elements[e].getAttribute('refid');
                                                    if (refid) {
                                                        usehyperlink = false;
                                                        gotoElement(refid);
                                                        stopRender = true;
                                                    }
                                                    else 
                                                        if (uri != null) {
                                                            usehyperlink = false;
                                                            if (uri.indexOf("file://") == 0) {
                                                                var tokens = uri.substring(7);
                                                                window.open(tokens);
                                                            }
                                                            else {
                                                                var tokens = (' ' + uri).split(/(\r\n|[\r\n])/g);
                                                                window.open(tokens[0]);
                                                            }
                                                            stopRender = true;
                                                        }
                                                }
                                            }
                                        }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    if (!stopRender) {
        var content = document.getElementById('content');
        if (usehyperlink) {
            usehyperlink = false;
            if (model.tagName == 'callbehavioraction') {
                var behaviorTags = model.getElementsByTagName('behavior');
                if (behaviorTags.length > 0) {
                    gotoElement(behaviorTags[0].getAttribute('refid'));
                }
                else {
                    renderElement(model);
                    var diagramtab = document.getElementById('diagramtab');
                    if (diagramtab) 
                        diagramtab.style.display = 'none';
                    selectView('specification');
                }
            }
            else 
                if (model.tagName == 'state') {
                    var submachineTags = model.getElementsByTagName('submachine');
                    if (submachineTags.length > 0) {
                        gotoElement(submachineTags[0].getAttribute('refid'));
                    }
                    else {
                        renderElement(model);
                        var diagramtab = document.getElementById('diagramtab');
                        if (diagramtab) 
                            diagramtab.style.display = 'none';
                        selectView('specification');
                    }
                }
                else 
                    if (model.tagName == 'collaboration') {
                        content.model = model;
                        var interaction = model.getElementsByTagName('interaction');
                        if (interaction.length > 0) {
                            XMLRequest.send(resourcesLocation + 'xml/' + interaction[0].getAttribute('refid') + '.xml', function(responseXML){
                                var magicdraw;
                                if (responseXML) 
                                    magicdraw = responseXML.getElementsByTagName('magicdraw')[0];
                                if (magicdraw == null) {
                                    alert('This element was not generated from project.');
                                    return;
                                }
                                var interaction = firstChild(magicdraw);
                                var diagram = interaction.getElementsByTagName('diagram');
                                if (diagram.length > 0) {
                                    XMLRequest.send(resourcesLocation + 'xml/' + diagram[0].getAttribute('refid') + '.xml', function(responseXML){
                                        var magicdraw;
                                        if (responseXML) 
                                            magicdraw = responseXML.getElementsByTagName('magicdraw')[0];
                                        if (magicdraw == null) {
                                            alert('This element was not generated from project.');
                                            return;
                                        }
                                        var diagram = firstChild(magicdraw);
                                        var content = document.getElementById('content');
                                        if (content != null) {
                                            renderDiagram(content.model, diagram);
                                            selectView('diagram');
                                        }
                                    });
                                }
                                else {
                                    renderElement(model);
                                    var diagramtab = document.getElementById('diagramtab');
                                    if (diagramtab) 
                                        diagramtab.style.display = 'none';
                                    selectView('specification');
                                }
                            });
                        }
                        else {
                            renderElement(model);
                            var diagramtab = document.getElementById('diagramtab');
                            if (diagramtab) 
                                diagramtab.style.display = 'none';
                            selectView('specification');
                        }
                    }
                    else 
                        if (model.tagName == 'activity' ||
                        model.tagName == 'statemachine' ||
                        model.tagName == 'interaction' ||
                        model.tagName == 'protocolstatemachine' ||
                        model.tagName == 'opaquebehavior' ||
                        model.tagName == 'functionalbehavior') {
                            var diagramTags = model.getElementsByTagName('diagram');
                            if (diagramTags.length > 0) {
                                content.model = model;
                                XMLRequest.send(resourcesLocation + 'xml/' + diagramTags[0].getAttribute('refid') + '.xml', function(responseXML){
                                    var magicdraw;
                                    if (responseXML) 
                                        magicdraw = responseXML.getElementsByTagName('magicdraw')[0];
                                    if (magicdraw == null) {
                                        alert('This element was not generated from project.');
                                        return;
                                    }
                                    var diagram = firstChild(magicdraw);
                                    var content = document.getElementById('content');
                                    if (content != null) {
                                        renderDiagram(content.model, diagram);
                                        selectView('diagram');
                                    }
                                });
                            }
                            else {
                                renderElement(model);
                                var diagramtab = document.getElementById('diagramtab');
                                if (diagramtab) 
                                    diagramtab.style.display = 'none';
                                selectView('specification');
                            }
                        }
                        else 
                            if (model.tagName == 'diagram') {
                                renderDiagram(model);
                                selectView('diagram');
                            }
                            else {
                                renderElement(model);
                                var diagramtab = document.getElementById('diagramtab');
                                if (diagramtab) 
                                    diagramtab.style.display = 'none';
                                selectView('specification');
                            }
        }
        else 
            if (model.tagName == 'diagram') {
                renderDiagram(model);
                selectView('diagram');
            }
            else {
                renderElement(model);
                var diagramtab = document.getElementById('diagramtab');
                if (diagramtab) 
                    diagramtab.style.display = 'none';
                selectView('specification');
            }
        var modelId = model.getAttribute('id');
        content.refid = modelId;
        if (modelId) {
            if (backStack.peek() != modelId) {
                backStack.push(modelId);
                if (backStack.size() > 1) {
                    var backButton = document.getElementById('backButton');
                    if (backButton != null) 
                        backButton.className = 'back';
                }
            }
            currentPageId = modelId;
            if (!useStack) {
                forwardStack.clear();
                var forwardButton = document.getElementById('forwardButton');
                if (forwardButton != null) 
                    forwardButton.className = 'forwardDisabled';
            }
        }
        repaint();
    }
}

/**
 * Store review stereotype.
 */
function Review(no, text, author, date){
    this.no = no;
    this.text = text;
    this.author = author;
    this.date = date;
}

/**
 * Store hyperlink stereotype.
 * @param {String} id
 * @param {String} name
 * @param {String} icon
 * @param {boolean} isModel
 */
function ModelLink(id, name, icon, isModel){
    this.id = id;
    this.name = name;
    this.icon = icon;
    this.isModel = isModel;
}

/**
 * Element specification renderer.
 */
function renderElement(model){
    var content = document.getElementById('content');
    content.model = model;
    removeAll(content);
    content.appendChild(createActionBar());
    content.appendChild(createViewBar(model));
    var header = document.createElement('h2');
    header.id = 'contentHeader';
    header.appendChild(document.createTextNode(model.getAttribute('humanType')));
    if (navigator.userAgent.indexOf('MSIE 6') >= 0) 
        header.style.marginTop = '2em';
    content.appendChild(header);
    if (model.hasChildNodes) {
        var table = document.createElement('div');
        table.className = 'table';
        var thead = document.createElement('div');
        thead.className = 'thead';
        thead.appendChild(document.createTextNode('General Information'));
        table.appendChild(thead);
        var tbody = document.createElement('div');
        tbody.id = 'generalTable';
        tbody.className = 'tbody';
        table.appendChild(tbody);
        content.appendChild(table);
        // permanent link
        var row = document.createElement('div');
        row.className = 'row';
        var label = document.createElement('label');
        label.appendChild(document.createTextNode('Link'));
        row.appendChild(label);
        var separator = document.createElement('span');
        separator.className = 'col';
        separator.appendChild(document.createTextNode(' : '));
        row.appendChild(separator);
        var value = document.createElement('span');
        value.className = 'col';
        var linkAnchor = document.createElement('a');
        linkAnchor.target = '_blank';
        linkAnchor.href = new String(window.location.protocol + "//" + window.location.host + window.location.pathname + '?refid=' + model.getAttribute('id'));
        linkAnchor.innerHTML = linkAnchor.href;
        value.appendChild(linkAnchor);
        row.appendChild(value);
        table.appendChild(row);
        // peoperties
        var reviewList = new Array();
        var childNodes = model.childNodes;
        for (var c = 0; c < childNodes.length; c++) {
            if (childNodes[c].tagName == 'name') 
                header.appendChild(document.createTextNode(' ' + nodeValue(childNodes[c])));
            if (childNodes[c].nodeType == 1) {
                // Stereotype
                if (childNodes[c].tagName == 'appliedStereotype') {
                    if (childNodes[c].hasChildNodes) {
                        var stereotypes = childNodes[c].childNodes;
                        for (var s = 0; s < stereotypes.length; s++) {
                            var stereotypeName = stereotypes[s].getAttribute('name');
                            // if review stereotype
                            if (stereotypeName == 'review') {
                                var properties = stereotypes[s].childNodes;
                                for (var p = 0; p < properties.length; p++) {
                                    if (properties[p].firstChild && properties[p].firstChild.nodeType == 1) {
                                        var name = properties[p].getAttribute('name');
                                        var collections = properties[p].childNodes;
                                        for (var o = 0; o < collections.length; o++) {
                                            var review;
                                            if (reviewList.length > o) 
                                                review = reviewList[o];
                                            else {
                                                review = new Review();
                                                reviewList.push(review);
                                            }
                                            review.no = o;
                                            eval('review.' + name + '=nodeValue(collections[' + o + ']);');
                                        }
                                    }
                                }
                                continue;
                            }
                            // continue on stereotype
                            var stable = document.createElement('div');
                            stable.className = 'table';
                            var sthead = document.createElement('div');
                            sthead.className = 'thead';
                            sthead.appendChild(document.createTextNode(stereotypes[s].getAttribute('humanType') + ' ' + stereotypes[s].getAttribute('name')));
                            stable.appendChild(sthead);
                            var stbody = document.createElement('div');
                            stbody.id = stereotypes[s].getAttribute('refid');
                            stbody.className = 'tbody';
                            stable.appendChild(stbody);
                            content.appendChild(stable);
                            var properties = stereotypes[s].childNodes;
                            for (var p = 0; p < properties.length; p++) {
                                if (properties[p].firstChild && properties[p].firstChild.nodeType == 1) {
                                    var row = document.createElement('div');
                                    row.className = 'row';
                                    var label = document.createElement('label');
                                    label.appendChild(document.createTextNode(properties[p].getAttribute('humanName')));
                                    row.appendChild(label);
                                    var separator = document.createElement('span');
                                    separator.className = 'col';
                                    separator.appendChild(document.createTextNode(' : '));
                                    row.appendChild(separator);
                                    var value = document.createElement('span');
                                    value.className = 'col';
                                    var collections = properties[p].childNodes;
                                    for (var o = 0; o < collections.length; o++) {
                                        if (collections[o].getAttribute('refid')) 
                                            createLink(value, collections[o]);
                                        else 
                                            renderValueNode(value, collections[o]);
                                        value.appendChild(document.createElement('br'));
                                    }
                                    row.appendChild(value);
                                    stbody.appendChild(row);
                                }
                            }
                        }
                    }
                    continue;
                }
                else 
                    if (childNodes[c].tagName == 'documentation') {
                        var dtable = document.createElement('div');
                        dtable.className = 'table';
                        var dthead = document.createElement('div');
                        dthead.className = 'thead';
                        dthead.appendChild(document.createTextNode(childNodes[c].getAttribute('humanName')));
                        dtable.appendChild(dthead);
                        var dtbody = document.createElement('div');
                        dtbody.id = 'documentationTable';
                        dtbody.className = 'tbody';
                        dtable.appendChild(dtbody);
                        content.appendChild(dtable);
                        var row = document.createElement('div');
                        row.className = 'row';
                        var value = document.createElement('div');
                        renderValueNode(value, childNodes[c]);
                        row.appendChild(value);
                        dtbody.appendChild(row);
                        continue;
                    }
                // General Information
                if (childNodes[c].tagName == 'map') 
                    continue;
                var showProperty = false;
                if (content.mode == '') 
                    showProperty = true;
                else {
                    var mode = childNodes[c].getAttribute('mode');
                    if (mode) 
                        showProperty = mode.indexOf(content.mode) >= 0;
                }
                if (showProperty) {
                    var row = document.createElement('div');
                    row.className = 'row';
                    var label = document.createElement('label');
                    label.appendChild(document.createTextNode(childNodes[c].getAttribute('humanName')));
                    row.appendChild(label);
                    var separator = document.createElement('span');
                    separator.className = 'col';
                    separator.appendChild(document.createTextNode(' : '));
                    row.appendChild(separator);
                    var value = document.createElement('span');
                    value.className = 'col';
                    if (childNodes[c].firstChild && childNodes[c].firstChild.nodeType == 1) {
                        var collections = childNodes[c].childNodes;
                        var cdiv = document.createElement('div');
                        cdiv.className = 'none';
                        cdiv.id = childNodes[c].getAttribute('humanName');
                        if (collections.length > 1) {
                            var img = document.createElement('img');
                            img.src = Content.imgShow;
                            img.alt = '';
                            img.className = 'toggle';
                            img.contentId = cdiv.id;
                            img.onclick = function(){
                                var content = new Content();
                                content.imgHide = resourcesLocation + 'images/left_triangle.gif';
                                content.showHide(this, this.contentId);
                            };
                            row.appendChild(img);
                        }
                        value.appendChild(cdiv);
                        for (var o = 0; o < collections.length; o++) {
                            var humanType = collections[o].getAttribute('humanType');
                            if (humanType) 
                                createLink(cdiv, collections[o]);
                            else 
                                renderValueNode(cdiv, collections[o]);
                            cdiv.appendChild(document.createElement('br'));
                        }
                    }
                    else {
                        var humanType = childNodes[c].getAttribute('humanType');
                        if (humanType) 
                            createLink(value, childNodes[c]);
                        else 
                            renderValueNode(value, childNodes[c]);
                    }
                    row.appendChild(value);
                    tbody.appendChild(row);
                }
            }
        }
    }
    renderReviewBox(reviewList);
}

function createContextItem(container, icon, label, func, href, refid){
    var liitem = document.createElement('li');
    var link = document.createElement('a');
    if (href != null && href != "") {
        if (href.indexOf("file://") == 0) 
            link.href = href.substring(7);
        else 
            link.href = href;
        link.target = "_blank";
    }
    else {
        link.href = 'javascript:void(0);';
    }
    var linkIcon = document.createElement('img');
    linkIcon.alt = '';
    linkIcon.border = '0';
    linkIcon.heigth = '16';
    linkIcon.width = '16';
    linkIcon.style.padding = '2px 5px 2px 5px';
	 if(refid != null && refid != "")
      linkIcon.refid = refid;
    linkIcon.onclick = func;
    linkIcon.src = icon;
	 if(refid != null && refid != "")
      link.refid = refid;
    link.onclick = func;
    link.appendChild(linkIcon);
    link.appendChild(document.createTextNode(label));
    liitem.appendChild(link);
    if (container != null) {
        var i = container.hasChildNodes() ? container.childNodes.length : 0;
        liitem.id = 'elementContextItem' + i;
        linkIcon.id = 'elementContextItemIcon' + i;
        link.id = 'elementContextItemLink' + i;
        container.appendChild(liitem);
    }
    return liitem;
}

/**
 * Diagram specification renderer.
 */
function renderDiagram(model, diagamModel){
    var specIcon;
    var content = document.getElementById('content');
    content.model = model;
    content.diagamModel = diagamModel;
    removeAll(content);
    content.appendChild(createActionBar());
    content.appendChild(createViewBar(model));
    if (diagamModel) 
        model = diagamModel;
    var header = document.createElement('h2');
    header.id = 'contentHeader';
    header.appendChild(document.createTextNode(model.getAttribute('diagramType')));
    if (navigator.userAgent.indexOf('MSIE 6') >= 0) 
        header.style.marginTop = '2em';
    content.appendChild(header);
    var mapName;
    var areas;
    var ulcontext = null;
    if (model.hasChildNodes) {
        mapName = 'map_' + model.getAttribute('id');
        var childNodes = model.childNodes;
        for (var c = 0; c < childNodes.length; c++) {
            if (childNodes[c].tagName == 'name') 
                header.appendChild(document.createTextNode(' ' + nodeValue(childNodes[c])));
            else 
                if (childNodes[c].tagName == 'map') {
                    var map = document.createElement('map');
                    map.id = mapName;
                    map.setAttribute('name', mapName);
                    if (childNodes[c].hasChildNodes) {
                        areas = childNodes[c].childNodes;
                        var elementArea = new Array();
                        for (a = 0; a < areas.length; a++) {
                            elementArea[a] = document.createElement('area');
                            elementArea[a].shape = 'poly';
                            elementArea[a].alt = areas[a].getAttribute('name');
                            elementArea[a].id = a;
                            elementArea[a].href = 'javascript:void(0);';
                            elementArea[a].ondblclick = function(e){
                                var elementId = areas[this.id].getAttribute('refid');
                                gotoElement(elementId);
                            };
                            elementArea[a].onmousedown = function(e){
                                evt = e ? e : event;
                                var elementId = areas[this.id].getAttribute('refid');
                                var id = this.id;
                                if (usecontextmenu) {
                                    XMLRequest.send(resourcesLocation + 'xml/' + elementId + '.xml', function(responseXML){
                                        var hyperlinkModel = new Array();
                                        var hyperlinkText = new Array();
                                        var hyperlinkModelActive;
                                        var hyperlinkTextActive;
                                        var magicdraw;
                                        if (responseXML) 
                                            magicdraw = responseXML.getElementsByTagName('magicdraw')[0];
                                        if (magicdraw != null) {
                                            var model = firstChild(magicdraw);
                                            specIcon = model.getAttribute('icon');
                                            hyperlinkModelActive = getActiveHyperlinkModel(model);
                                        }
                                        var model = null;
                                        if (magicdraw != null) {
                                            model = firstChild(magicdraw);
                                            if (model.hasChildNodes) {
                                                var childNodes = model.childNodes;
                                                for (var i = 0; i < childNodes.length; i++) {
                                                    if (childNodes[i].tagName == 'appliedStereotype') {
                                                        if (childNodes[i].hasChildNodes) {
                                                            var stereotypes = childNodes[i].childNodes;
                                                            for (s = 0; s < stereotypes.length; s++) {
                                                                var stereotypesName = stereotypes[s].getAttribute('name')
                                                                if (stereotypesName == 'HyperlinkOwner') {
                                                                    if (stereotypes[s].hasChildNodes) {
                                                                        var properties = stereotypes[s].childNodes;
                                                                        for (p = 0; p < properties.length; p++) {
                                                                            var propertyName = properties[p].getAttribute('name');
                                                                            if (propertyName == 'hyperlinkModel') {
                                                                                if (properties[p].hasChildNodes) {
                                                                                    var elements = properties[p].childNodes;
                                                                                    for (var e = 0; e < elements.length; e++) {
                                                                                        var refid = elements[e].getAttribute('refid');
                                                                                        if (hyperlinkModelActive && hyperlinkModelActive.id) {
                                                                                            if (refid != hyperlinkModelActive.id) {
                                                                                                hyperlinkModel.push(new ModelLink(refid, elements[e].getAttribute('name'), elements[e].getAttribute('icon')))
                                                                                            }
                                                                                        }
                                                                                        else {
                                                                                            hyperlinkModel.push(new ModelLink(refid, elements[e].getAttribute('name'), elements[e].getAttribute('icon')))
                                                                                        }
                                                                                    }
                                                                                }
                                                                            }
                                                                            else if (propertyName == 'hyperlinkText') {
                                                                                    if (properties[p].hasChildNodes) {
                                                                                        var elements = properties[p].childNodes;
                                                                                        for (var e = 0; e < elements.length; e++) {
                                                                                            if (elements[e].tagName == "String") {
                                                                                                if (elements[e].hasChildNodes) {
                                                                                                    var linkText = elements[e].childNodes;
                                                                                                    hyperlinkText.push(new ModelLink(linkText[0].nodeValue, linkText[0].nodeValue, resourcesLocation + 'images/hyperlink_url.gif', false))
                                                                                                }
                                                                                            }
                                                                                            else {
                                                                                                var refid = elements[e].getAttribute('refid');
                                                                                                if (hyperlinkModelActive && hyperlinkModelActive.id) {
                                                                                                    if (refid != hyperlinkModelActive.id) {
                                                                                                        hyperlinkText.push(new ModelLink(refid, elements[e].getAttribute('name'), elements[e].getAttribute('icon'), true))
                                                                                                    }
                                                                                                }
                                                                                                else {
                                                                                                    hyperlinkText.push(new ModelLink(refid, elements[e].getAttribute('name'), elements[e].getAttribute('icon'), true))
                                                                                                }
                                                                                            }
                                                                                        }
                                                                                    }
                                                                                }
                                                                                else if (propertyName == 'hyperlinkTextActive') {
                                                                                        if (properties[p].hasChildNodes) {
                                                                                            var elements = properties[p].childNodes;
                                                                                            for (var e = 0; e < elements.length; e++) {
                                                                                                if (elements[e].tagName == "String") {
                                                                                                    if (elements[e].hasChildNodes) {
                                                                                                        var linkText = elements[e].childNodes;
                                                                                                        hyperlinkTextActive = new ModelLink(linkText[0].nodeValue, linkText[0].nodeValue, resourcesLocation + 'images/hyperlink_url.gif', false);
                                                                                                    }
                                                                                                }
                                                                                                else {
                                                                                                    var refid = elements[e].getAttribute('refid');
                                                                                                    if (hyperlinkModelActive && hyperlinkModelActive.id) {
                                                                                                        if (refid != hyperlinkModelActive.id) {
                                                                                                            hyperlinkTextActive = new ModelLink(refid, elements[e].getAttribute('name'), elements[e].getAttribute('icon'), true);
                                                                                                            
                                                                                                        }
                                                                                                    }
                                                                                                    else {
                                                                                                        hyperlinkTextActive = new ModelLink(refid, elements[e].getAttribute('name'), elements[e].getAttribute('icon'), true);
                                                                                                    }
                                                                                                }
                                                                                                
                                                                                            }
                                                                                        }
                                                                                    }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                        
                                        ulcontext = document.getElementById('elementcontextmenu');
                                        if (ulcontext == null) {
                                            ulcontext = document.createElement('ul');
                                            ulcontext.id = 'elementcontextmenu';
                                            ulcontext.className = 'contextMenu';
                                        }
                                        removeAll(ulcontext);
                                        // specification
                                        var liitem = createContextItem(ulcontext, specIcon, 'Specification', function(){
                                            showSpec(areas[id].getAttribute('refid'));
                                        });
                                        // active model
                                        if (hyperlinkModelActive) {
                                            liitem = createContextItem(ulcontext, hyperlinkModelActive.icon, 'Go to ' + hyperlinkModelActive.name, function(){
                                                gotoElement(areas[id].getAttribute('refid'));
                                            });
                                        }
                                        // active text
                                        if (hyperlinkTextActive) {
                                            if (!hyperlinkTextActive.isModel) {
                                                liitem = createContextItem(ulcontext, hyperlinkTextActive.icon, hyperlinkTextActive.name, function(){
                                                    var elementContext = document.getElementById('elementcontextmenu');
                                                    if (elementContext) {
                                                        elementContext.style.visibility = 'hidden';
                                                        Shadow.removeShadow(elementContext);
                                                    }
                                                }, hyperlinkTextActive.name);
                                            }
                                            else {
                                                liitem = createContextItem(ulcontext, hyperlinkTextActive.icon, 'Go to ' + hyperlinkTextActive.name, function(){
                                                    gotoElement(hyperlinkTextActive.id);
                                                });
                                                
                                            }
                                        }
                                        // model links
                                        var liitemIndex = liitem.length;
                                        for (var h = 0; h < hyperlinkModel.length; h++) {
                                            liitem = createContextItem(ulcontext, hyperlinkModel[h].icon, 'Go to ' + hyperlinkModel[h].name, function(){
                                                showSpec(this.refid);
                                            },"", hyperlinkModel[h].id);
                                        }
                                        // text links
                                        var liitemIndex = liitem.length;
                                        for (var h = 0; h < hyperlinkText.length; h++) {
                                            if (hyperlinkTextActive == null || hyperlinkText[h].id != hyperlinkTextActive.id) {
                                                if (!hyperlinkText[h].isModel) {
                                                    liitem = createContextItem(ulcontext, hyperlinkText[h].icon, hyperlinkText[h].name, function(){
                                                        var elementContext = document.getElementById('elementcontextmenu');
                                                        if (elementContext) {
                                                            elementContext.style.visibility = 'hidden';
                                                            Shadow.removeShadow(elementContext);
                                                        }
                                                    }, hyperlinkText[h].name);
                                                }
                                                else {
                                                    liitem = createContextItem(ulcontext, hyperlinkText[h].icon, 'Go to ' + hyperlinkText[h].name, function(){
                                                        gotoElement(this.refid);
                                                    }, "", hyperlinkText[h].id);
                                                }
                                            }
                                        }
                                        // state
                                        if (model) {
                                            if (model.tagName == 'state') {
                                                var submachineTags = model.getElementsByTagName('submachine');
                                                if (submachineTags.length > 0) {
                                                    liitem = createContextItem(ulcontext, submachineTags[0].getAttribute('icon'), 'Go to ' + submachineTags[0].name, function(){
                                                        gotoElement(submachineTags[0].getAttribute('refid'));
                                                    });
                                                }
                                            }
                                            // callbehavior
                                            else 
                                                if (model.tagName == 'callbehavior') {
                                                    var behaviorTags = model.getElementsByTagName('behavior');
                                                    if (behaviorTags.length > 0) {
                                                        liitem = createContextItem(ulcontext, behaviorTags[0].getAttribute('icon'), 'Go to ' + behaviorTags[0].name, function(){
                                                            gotoElement(behaviorTags[0].getAttribute('refid'));
                                                        });
                                                    }
                                                }
                                        }
                                        // show context menu
                                        var mic = Graphics.mousePosition(evt);
                                        var mouseX = mic.x + 2;
                                        var mouseY = mic.y + 2;
                                        ulcontext.style.position = 'absolute';
                                        ulcontext.style.left = mouseX + 'px';
                                        ulcontext.style.top = mouseY + 'px';
                                        ulcontext.style.display = 'block';
                                        ulcontext.style.visibility = 'visible';
                                        ulcontext.style.zIndex = (content.style.zIndex ? content.style.zIndex : 133) + 100;
                                        content.appendChild(ulcontext);
                                        Shadow.castShadow(ulcontext);
                                    });
                                }
                                else {
                                    gotoElement(elementId);
                                }
                            }
                            var points = areas[a].childNodes;
                            var coordsString = "";
                            for (var p = 0; p < points.length; p++, coordsString += ',') {
                                coordsString += points[p].getAttribute('x') + ',' + points[p].getAttribute('y');
                            }
                            coordsString += points[0].getAttribute('x') + ',' + points[0].getAttribute('y');
                            elementArea[a].coords = coordsString;
                            map.appendChild(elementArea[a]);
                        }
                    }
                    content.appendChild(map);
                }
        }
    }
    
    document.body.onmousedown = function(e){
        var evt = e ? e : event;
        var target = evt.target ? evt.target : evt.srcElement;
        var targetNodeName = target.nodeName;
        var targetNodeId = target.id;
        
        if (!(targetNodeName == "AREA" || (targetNodeId != null && targetNodeId.indexOf("elementContextItem") == 0))) {
            var contextMenu = document.getElementById('elementcontextmenu');
            if (contextMenu) {
                contextMenu.style.disply = 'none';
                contextMenu.style.visibility = 'hidden';
                Shadow.removeShadow(contextMenu);
            }
        }
    }
    
    var diagramContainer = document.createElement('div');
    diagramContainer.id = 'diagramContainer';
    var imagePath = model.getAttribute('src');
    var imageFormat = imagePath.substring(imagePath.lastIndexOf(".") + 1, imagePath.length);
    var image;
    if (imageFormat == 'svg') 
        image = document.createElement('embed');
    else 
        image = document.createElement('img');
    image.src = model.getAttribute('src');
    image.width = model.getAttribute('width');
    image.height = model.getAttribute('height');
    image.alt = ''; // model.getAttribute('diagramType');
    image.border = '0';
    image.className = 'diagram';
    if (mapName) 
        image.useMap = '#' + mapName;
    diagramContainer.appendChild(image);
    content.appendChild(diagramContainer);
}

/**
 * Return an active hyperlink attached to this model.
 * @param {HTML} model
 * @return ModelLink or null
 */
function getActiveHyperlinkModel(model){
    if (model && model.hasChildNodes) {
        var childNodes = model.childNodes;
        for (var i = 0; i < childNodes.length; i++) {
            if (childNodes[i].tagName == 'appliedStereotype') {
                if (childNodes[i].hasChildNodes) {
                    var stereotypes = childNodes[i].childNodes;
                    for (s = 0; s < stereotypes.length; s++) {
                        var stereotypesName = stereotypes[s].getAttribute('name')
                        if (stereotypesName == 'HyperlinkOwner') {
                            if (stereotypes[s].hasChildNodes) {
                                var properties = stereotypes[s].childNodes;
                                for (p = 0; p < properties.length; p++) {
                                    var propertyName = properties[p].getAttribute('name');
                                    if (propertyName == 'hyperlinkModelActive') {
                                        if (properties[p].hasChildNodes) {
                                            var element = properties[p].childNodes;
                                            if (element[0] != null) {
                                                return new ModelLink(element[0].getAttribute('refid'), element[0].getAttribute('name'), element[0].getAttribute('icon'))
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return null;
}

/**
 * Append a review box to table.
 */
function renderReviewBox(reviewList){
    var content = document.getElementById('content');
    // render review history
    if (reviewList.length > 0) {
        var rtable = document.createElement('div');
        rtable.className = 'table';
        var rthead = document.createElement('div');
        rthead.className = 'thead';
        rthead.appendChild(document.createTextNode('Review'));
        rtable.appendChild(rthead);
        var rtbody = document.createElement('div');
        rtbody.id = 'reviewHistoryTable';
        rtbody.className = 'tbody';
        rtable.appendChild(rtbody);
        content.appendChild(rtable);
        for (var i = 0; i < reviewList.length; i++) {
            var review = reviewList[i];
            var row = document.createElement('div');
            row.className = 'row';
            var valueSect = document.createElement('span');
            var text = review.text;
            var startBodyIndex = text.indexOf('<body>');
            var endBodyIndex = text.indexOf('</body>', startBodyIndex);
            if (startBodyIndex > 0 && endBodyIndex > 0) 
                text = text.substring(startBodyIndex, endBodyIndex);
            valueSect.innerHTML = review.text;
            var authorSect = document.createElement('p');
            authorSect.style.marginTop = '20px';
            authorSect.style.fontStyle = 'italic';
            authorSect.style.color = '#888888';
            authorSect.appendChild(document.createTextNode(review.author + ' (' + review.date + ' )'));
            valueSect.appendChild(authorSect);
            row.appendChild(valueSect);
            rtbody.appendChild(row);
        }
    }
}

/**
 * Goto element.
 * @elementId element id
 */
function gotoElement(elementId, keepStack){
    usehyperlink = true;
    useStack = keepStack;
    XMLRequest.send(resourcesLocation + 'xml/' + elementId + '.xml', renderModel);
}

/**
 * Show element's specification page
 * @param elementId element id
 * @param keepStack put command into undo stack
 */
function showSpec(elementId, keepStack){
    usehyperlink = false;
    useStack = keepStack;
    XMLRequest.send(resourcesLocation + 'xml/' + elementId + '.xml', renderModel);
}

/**
 * Expand node path
 */
function expandPath(nodePath){
    stopexpand = false;
    var rootTree = document.getElementById(tree.treeId);
    var path = nodePath.length - 1;
    internalExpandPath(rootTree, nodePath, path);
}

/** we already found node stop searching and collapse investigating node */
var stopexpand = false;
function internalExpandPath(rootNode, nodePath, path){
    if (path < 0 || stopexpand) 
        return;
    var childNodes = rootNode.childNodes;
    var content = document.getElementById('content');
    if (childNodes) {
        for (var c = 0; c < childNodes.length; c++) {
            if (childNodes[c].tagName == 'UL') 
                internalExpandPath(childNodes[c], nodePath, path);
            else 
                if (childNodes[c].tagName == 'LI') {
                    var refid = childNodes[c].getAttribute('refid');
                    childNodes[c].internalExpand = false;
                    if (refid == 'relations') {
                        // if node already expand, left it expand
                        if (childNodes[c].lastChild && !childNodes[c].lastChild.isExpanded) {
                            tree.expand(childNodes[c]);
                            // mark as node is expanded for investigating
                            childNodes[c].internalExpand = true;
                        }
                        internalExpandPath(childNodes[c], nodePath, path);
                    }
                    else 
                        if (refid == nodePath[path]) {
                            // if node already expand, left it expand
                            if (childNodes[c].lastChild && !childNodes[c].lastChild.isExpanded) {
                                tree.expand(childNodes[c]);
                                // mark as node is expanded for investigating
                                childNodes[c].internalExpand = true;
                            }
                            internalExpandPath(childNodes[c], nodePath, --path);
                        }
                    // if found target node then stop expanding
                    if (path == -1) 
                        stopexpand = true;
                    if (!stopexpand) {
                        // collapse node that use for investigating.
                        if (childNodes[c].internalExpand) 
                            tree.collapse(childNodes[c]);
                    }
                }
        }
    }
}

/**
 * Goto last visit page
 */
function back(){
    if (backStack.size() == 1) 
        return;
    backStack.pop();
    var lastPageId = backStack.pop();
    if (backStack.size() < 1) {
        var backButton = document.getElementById('backButton');
        backButton.className = 'backDisabled';
    }
    if (lastPageId) {
        forwardStack.push(currentPageId);
        var forwardButton = document.getElementById('forwardButton');
        forwardButton.className = 'forward';
        showSpec(lastPageId, true);
        var node = findNode(lastPageId);
        if (node) 
            selectNode(node);
    }
}

/**
 * Forward to next visit page
 */
function forward(){
    var lastPageId = forwardStack.pop();
    if (forwardStack.size() < 1) {
        var forwardButton = document.getElementById('forwardButton');
        forwardButton.className = 'forwardDisabled';
    }
    if (lastPageId) {
        gotoElement(lastPageId, true);
        var node = findNode(lastPageId);
        if (node) 
            selectNode(node);
    }
}

/**
 * Trim string
 * @param input string
 * @return output string
 */
function trim(aB){
    return aB.replace(/^\s*|\s*$/g, '');
}

/**
 * Test matches node with regular expression
 */
function match(node, attr, regx, searchResults){
    if (node.tagName == 'ownedDiagram') 
        return;
    if (node.nodeType == 1) {
        var name = node.getAttribute(attr);
        if ((name == '' || name) && regx.test(name)) 
            searchResults[searchResults.length] = node;
    }
    if (node.hasChildNodes()) {
        var childNodes = node.childNodes;
        for (var i = 0; i < childNodes.length; i++) 
            match(childNodes[i], attr, regx, searchResults);
    }
}

/**
 * Search function. Regular expression can be used with element name.
 * @param elementName name of element being search.
 */
function search(elementName){
    if (tree.root) {
        showLoading();
        var dataModel = tree.root.firstChild.data;
        var regx;
        try {
            regx = new RegExp(trim(elementName), 'i');
        } 
        catch (e) {
            alert('Invalid search pattern \nReason: ' + e.message + '\nPlease validate regular expression syntax in search text');
        }
        if (regx) {
            var searchResults = new Array(0);
            match(dataModel, 'name', regx, searchResults);
            var content = document.getElementById('content');
            removeAll(content);
            var header = document.createElement('h2');
            header.id = 'contentHeader';
            header.appendChild(document.createTextNode('Search Results'));
            content.appendChild(header);
            if (searchResults.length > 0) {
                var stable = document.createElement('div');
                stable.className = 'table';
                var sthead = document.createElement('div');
                sthead.className = 'thead';
                sthead.appendChild(document.createTextNode('Search Results'));
                stable.appendChild(sthead);
                var stbody = document.createElement('div');
                stbody.className = 'tbody';
                stable.appendChild(stbody);
                content.appendChild(stable);
                for (var p = 0; p < searchResults.length; p++) {
                    if (searchResults[p].nodeType == 1) {
                        var row = document.createElement('div');
                        row.className = 'row';
                        var name = document.createElement('span');
                        name.style.verticalAlign = 'middle';
                        createLink(name, searchResults[p]);
                        row.appendChild(name);
                        var type = document.createElement('span');
                        type.style.verticalAlign = 'middle';
                        type.appendChild(document.createTextNode(searchResults[p].getAttribute('humanType')));
                        row.appendChild(type);
                        stbody.appendChild(row);
                    }
                }
                repaint();
            }
            else {
                var message = document.createElement('h5');
                message.style.padding = '1em';
                message.appendChild(document.createTextNode('No element name containing all your search terms were found.'));
                content.appendChild(message);
            }
        }
        hideLoading();
    }
}

//custom loading dialog
loadingDialog = {
    show: function(){
        var popup = document.getElementById('popup');
        if (!popup) {
            popup = document.createElement('div');
            popup.setAttribute('id', 'popup');
            popup.innerHTML = '<span class="loading">Loading...</span>';
            document.body.appendChild(popup);
        }
    },
    
    hide: function(){
        var popup = document.getElementById('popup');
        if (popup) {
            document.body.removeChild(popup);
        }
    }
}
