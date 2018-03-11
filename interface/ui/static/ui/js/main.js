
function loadConfigs() {
    $.get('/ui/deployment_config/', (c) => {
        console.log(c);
    });
}

$(document).ready(() => {
    loadConfigs();
});