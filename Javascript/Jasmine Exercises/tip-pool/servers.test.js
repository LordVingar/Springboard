describe("Servers test (with setup and tear-down)", function() {
  beforeEach(function () {
    // initialization logic
    serverNameInput.value = 'Alice';
  });

  it('should add a new server to allServers on submitServerInfo()', function () {
    submitServerInfo();

    expect(Object.keys(allServers).length).toEqual(1);
    expect(allServers['server' + serverId].serverName).toEqual('Alice');
  });
  
  it('should update serverTable with new server on submitServerInfo()', function () {
    submitServerInfo();

    const serverRows = serverTbody.querySelectorAll('tr');

    expect(serverRows.length).toEqual(1);
    expect(serverRows[0].querySelector('td').innerText).toEqual('Alice');
  });

  afterEach(function() {
    // teardown logic
    serverTbody.innerHTML = '';
    allServers = {};
    serverId = 0;
  });
});