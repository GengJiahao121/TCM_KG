import json
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher

# 连接数据库
graph = Graph("http://localhost:7474", auth=("neo4j", "123456789"),name="neo4j")

# graph.delete_all()
matcher_node = NodeMatcher(graph)
matcher_relation = RelationshipMatcher(graph)

with open("//root/autodl-tmp/TCM_KG-main/baseline_all_kg_triples.txt", "r", encoding="utf-8") as file:
    # i = 0
    for line in file.readlines():
        # i = i + 1
        # if i % 10000 == 0:
            # print(i)
        entity_1, entity_2, relation = line.split("\t")
        print(entity_1,"",entity_2,"",relation)

        # 使用NodeMatcher查找数据库中是否存在名为entity_1的节点，如果不存在则创建该节点
        node_1 = matcher_node.match(name=entity_1).first() # 查找
        if node_1 is None: # 如果不存在，创建一个结点，并加入到图中
            node_1 = Node(name=entity_1)
            graph.create(node_1)

        # relation为第二个节点的label
        node_2 = matcher_node.match(name=entity_2).first()
        if node_2 is None:
            node_2 = Node(relation, name=entity_2)
            graph.create(node_2)

            
        if not node_2.has_label(relation):
            # print(i)
            node_2.add_label(relation)
            graph.push(node_2)

        r = Relationship(node_1, relation, node_2)
        graph.create(r)

print("Done!")
'''
操作说明：
1.启动neo4j数据库：neo4j console
moc os系统启动neo4j数据库: /opt/homebrew/opt/neo4j/bin/neo4j console

2.启动neo4j可视化界面：http://localhost:7474/browser/

3.连接neo4j数据库：不知道用户名和密码怎么办

第一步：cd  /opt/homebrew/Cellar/neo4j/5.13.0/libexec/conf

修改：dbms.security.auth_enabled=true

第二步：cd /opt/homebrew/opt/neo4j/bin/

neo4j-admin dbms set-initial-password 123456789

4. 
"Bolt enabled on localhost:7687." 表示Bolt协议已在本地主机的7687端口上启用。Bolt是Neo4j数据库使用的二进制协议，用于与数据库进行通信。（网页与数据库通信）
"HTTP enabled on localhost:7474." 表示HTTP协议已在本地主机的7474端口上启用。Neo4j提供了HTTP接口，使用户能够通过浏览器或其他HTTP客户端与数据库进行交互。（http可视化页面）



这段代码是一个Python脚本，用于将存储在文件中的三元组数据导入到Neo4j图数据库中。让我逐步解释这段代码的功能：

import json: 导入json模块，尽管在代码中并没有使用它。

from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher: 从py2neo库导入所需的类和函数。py2neo是Neo4j的Python驱动程序，它提供了在Python中连接、查询和管理Neo4j数据库的功能。

graph = Graph("http://localhost:7474", auth=("neo4j", "123456789"), name="neo4j"): 创建一个Graph对象，用于连接到Neo4j数据库。使用提供的URL、用户名和密码来建立连接。URL是 http://localhost:7474，用户名是 "neo4j"，密码是 "123456789"。连接的名称为 "neo4j"。

with open("/Users/gjh/workspaces/vscode/python/5.TCM.python/TCM_KG-main/baseline_all_kg_triples.txt", "r", encoding="utf-8") as file:: 打开包含三元组数据的文本文件。

使用NodeMatcher和RelationshipMatcher来查找现有的节点和关系。

读取文本文件的每一行，并将每行的内容拆分为实体1、实体2和关系。

使用NodeMatcher查找数据库中是否存在名为entity_1的节点，如果不存在则创建该节点。

使用NodeMatcher查找数据库中是否存在名为entity_2的节点，如果不存在则创建该节点，并为节点添加标签为relation。

创建关系对象r，将node_1、relation和node_2作为关系的起始节点、类型和结束节点。

使用graph.create()方法将节点和关系对象保存到数据库中。

上述代码的目的是将文本文件中的三元组数据导入到Neo4j数据库中，并创建对应的节点和关系。每行三元组数据的格式是“实体1 实体2 关系”，它们将在数据库中表示为节点和关系。
'''