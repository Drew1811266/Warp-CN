use std::sync::LazyLock;

use regex::Regex;
use uuid::Uuid;

use crate::terminal::view::PromptSuggestion;

pub struct StaticPromptSuggestion {
    pub name: &'static str,
    pub pattern: &'static str,
    pub label_template: Option<&'static str>,
    pub query_template: &'static str,
}

/// Attempts to match a terminal command against predefined static prompt suggestions.
///
/// If the command matches a static rule, this returns a [`SuggestedQuery`] with details from the
/// command substituted into the rule's query template.
pub fn static_suggested_query(command: &str) -> Option<PromptSuggestion> {
    // Try each rule in turn and apply the first match.
    for pattern in &*RULE_PATTERNS {
        if let Some(captures) = pattern.regex.captures(command) {
            // If there's a match, apply placeholders to the query.
            let label = pattern
                .rule
                .label_template
                .map(|template| apply_captures(template, &captures));
            let query = apply_captures(pattern.rule.query_template, &captures);

            return Some(PromptSuggestion {
                id: Uuid::new_v4().to_string(),
                label,
                prompt: query,
                coding_query_context: None,
                static_prompt_suggestion_name: Some(pattern.rule.name.to_string()),
                should_start_new_conversation: false,
            });
        }
    }

    None
}

/// A static prompt suggestion with its pattern precompiled to a [`Regex`].
struct StaticPromptRule {
    rule: &'static StaticPromptSuggestion,
    regex: Regex,
}

static RULE_PATTERNS: LazyLock<Vec<StaticPromptRule>> = LazyLock::new(|| {
    STATIC_RULES
        .iter()
        .map(|rule| match Regex::new(rule.pattern) {
            Ok(regex) => StaticPromptRule { rule, regex },
            Err(e) => {
                panic!(
                    "Invalid pattern for static prompt rule `{}`: {}",
                    rule.name, e
                );
            }
        })
        .collect()
});

static STATIC_RULES: &[StaticPromptSuggestion] = &[
    // git checkout -b <branch>: Checks out a new branch named <branch>.
    StaticPromptSuggestion {
        name: "GIT_CHECKOUT_NEW_BRANCH",
        pattern: r"^git\s+checkout\s+-b\s+(\S+)\s*$",
        label_template: Some("在 {1} 中编写功能或修复 bug"),
        query_template: "在 {1} 中实现功能或修复 bug。请向我询问所需的所有细节。",
    },
    // git clone <repo>: Clones a repository named <repo>.
    StaticPromptSuggestion {
        name: "GIT_CLONE",
        pattern: r"^git\s+clone\s+(\S+)\s*$",
        label_template: Some("帮我在 {1} 中编写功能或修复 bug"),
        query_template: "在 {1} 中实现功能或修复 bug。请向我询问所需的所有细节。",
    },
    // git switch -c <branch>: Creates and switches to a new branch named <branch>.
    StaticPromptSuggestion {
        name: "GIT_SWITCH_NEW_BRANCH",
        pattern: r"^git\s+switch\s+-c\s+(\S+)\s*$",
        label_template: Some("在 {1} 中编写功能或修复 bug"),
        query_template: "在 {1} 中实现功能或修复 bug。请向我询问所需的所有细节。",
    },
    // git push: Pushes changes to a remote repository.
    StaticPromptSuggestion {
        name: "GIT_PUSH",
        pattern: r"^git\s+push\s*$",
        label_template: None,
        query_template: "帮我创建 pull request。",
    },
    // git init: Initializes a new, empty Git repository.
    StaticPromptSuggestion {
        name: "GIT_INIT",
        pattern: r"^git\s+init\s*$",
        label_template: Some("帮我开始一个新项目"),
        query_template: "帮我开始一个新项目。请向我询问所需的所有细节。",
    },
    // npm init / yarn init / pnpm init: Initializes a Node.js project.
    StaticPromptSuggestion {
        name: "NODE_PACKAGE_INIT",
        pattern: r"^(npm|yarn|pnpm)\s+init\s*$",
        label_template: Some("帮我开始一个 Node.js 项目"),
        query_template: "帮我开始一个 Node.js 项目。请向我询问所需的所有细节。",
    },
    // npx create-react-app <project>: Creates a new React app called <project>.
    StaticPromptSuggestion {
        name: "NPX_CREATE_REACT_APP",
        pattern: r"^npx\s+create-react-app\s+(\S+)\s*$",
        label_template: Some("帮我创建一个新的 React 应用"),
        query_template: "帮我创建一个名为 {1} 的新 React 应用。请向我询问所需的所有细节。",
    },
    // npx create-next-app <project>: Creates a new Next.js app called <project>.
    StaticPromptSuggestion {
        name: "NPX_CREATE_NEXT_APP",
        pattern: r"^npx\s+create-next-app\s+(\S+)\s*$",
        label_template: Some("帮我创建一个新的 Next.js 应用"),
        query_template: "帮我创建一个名为 {1} 的新 Next.js 应用。请向我询问所需的所有细节。",
    },
    // cargo new <project>: Creates a new Rust package named <project>.
    StaticPromptSuggestion {
        name: "CARGO_NEW_PROJECT",
        pattern: r"^cargo\s+new\s+(\S+)\s*$",
        label_template: Some("帮我为 {1} 开始一个 Rust 项目"),
        query_template: "帮我为 {1} 开始一个 Rust 项目。请向我询问所需的所有细节。",
    },
    // poetry new <project>: Creates a new Poetry-based Python project named <project>.
    StaticPromptSuggestion {
        name: "POETRY_NEW_PROJECT",
        pattern: r"^poetry\s+new\s+(\S+)\s*$",
        label_template: Some("帮我为 {1} 开始一个 Poetry 项目"),
        query_template: "帮我为 {1} 开始一个 Poetry 项目。请向我询问所需的所有细节。",
    },
    // django-admin startproject <project>: Creates a new Django project named <project>.
    StaticPromptSuggestion {
        name: "DJANGO_START_PROJECT",
        pattern: r"^django-admin\s+startproject\s+(\S+)\s*$",
        label_template: Some("帮我为 {1} 开始一个 Django 项目"),
        query_template: "帮我为 {1} 开始一个 Django 项目。请向我询问所需的所有细节。",
    },
    // rails new <app>: Creates a new Rails app named <app>.
    StaticPromptSuggestion {
        name: "RAILS_NEW_APP",
        pattern: r"^rails\s+new\s+(\S+)\s*$",
        label_template: Some("帮我为 {1} 开始一个 Rails 应用"),
        query_template: "帮我为 {1} 开始一个 Rails 应用。请向我询问所需的所有细节。",
    },
    // gradle init / mvn archetype:generate: Initializes a Gradle or Maven project.
    StaticPromptSuggestion {
        name: "JAVA_PROJECT_INIT",
        pattern: r"^(gradle\s+init|mvn\s+archetype:generate)\s*$",
        label_template: Some("帮我开始一个 Gradle/Maven 项目"),
        query_template: "帮我开始一个 Gradle/Maven 项目。请向我询问所需的所有细节。",
    },
    // go mod init <module>: Initializes a new Go module named <module>.
    StaticPromptSuggestion {
        name: "GO_MOD_INIT",
        pattern: r"^go\s+mod\s+init\s+(\S+)\s*$",
        label_template: Some("帮我为 {1} 开始一个 Go 项目"),
        query_template: "帮我为 {1} 开始一个 Go 项目。请向我询问所需的所有细节。",
    },
    // swift package init: Initializes a new Swift package.
    StaticPromptSuggestion {
        name: "SWIFT_PACKAGE_INIT",
        pattern: r"^swift\s+package\s+init\s*$",
        label_template: Some("帮我开始一个 Swift 项目"),
        query_template: "帮我开始一个 Swift 项目。请向我询问所需的所有细节。",
    },
    // terraform init: Initializes Terraform in the current directory.
    StaticPromptSuggestion {
        name: "TERRAFORM_INIT",
        pattern: r"^terraform\s+init\s*$",
        label_template: Some("帮我开始一个 Terraform 配置"),
        query_template: "帮我开始一个 Terraform 配置。请向我询问所需的所有细节。",
    },
    // prisma init: Initializes Prisma in the current project.
    StaticPromptSuggestion {
        name: "PRISMA_INIT",
        pattern: r"^prisma\s+init\s*$",
        label_template: Some("帮我在此项目中设置 Prisma"),
        query_template: "帮我在此项目中设置 Prisma。",
    },
    // python -m venv <env_name>: Creates a new Python virtual environment named <env_name>.
    StaticPromptSuggestion {
        name: "PYTHON_CREATE_VENV",
        pattern: r"^python\s+-m\s+venv\s+(\S+)\s*$",
        label_template: None,
        query_template: "帮我为 {1} 安装依赖。",
    },
    // bundle init: Creates a new Gemfile (Ruby Bundler).
    StaticPromptSuggestion {
        name: "BUNDLE_INIT",
        pattern: r"^bundle\s+init\s*$",
        label_template: Some("帮我设置一个新的 Ruby 项目"),
        query_template: "帮我设置一个新的 Ruby 项目。请向我询问所需的所有细节。",
    },
    // ollama pull <model>: Pulls an Ollama model named <model>.
    StaticPromptSuggestion {
        name: "OLLAMA_PULL_MODEL",
        pattern: r"^ollama\s+pull\s+(\S+)\s*$",
        label_template: None,
        query_template: "帮我为 {1} 设置模型文件（Modelfile）。",
    },
    // kubectl top nodes: Shows node resource usage in Kubernetes.
    StaticPromptSuggestion {
        name: "KUBECTL_TOP_NODES",
        pattern: r"^kubectl\s+top\s+(nodes|node|no)\s*$",
        label_template: None,
        query_template: "帮我了解集群中的资源利用率。",
    },
    // kubectl top pods: Shows pod resource usage in Kubernetes.
    StaticPromptSuggestion {
        name: "KUBECTL_TOP_PODS",
        pattern: r"^kubectl\s+top\s+(pods|po|pod)\s*$",
        label_template: None,
        query_template: "帮我了解集群中的资源利用率。",
    },
    // kubectl get...: Gets Kubernetes resources (any).
    StaticPromptSuggestion {
        name: "KUBECTL_GET_RESOURCES",
        pattern: r"^kubectl\s+get.*$",
        label_template: None,
        query_template: "帮我检查 Kubernetes 资源。",
    },
    // docker ps: Lists Docker containers.
    StaticPromptSuggestion {
        name: "DOCKER_LIST_CONTAINERS",
        pattern: r"^docker\s+ps\s*$",
        label_template: None,
        query_template: "帮我管理正在运行的容器。",
    },
    // docker image ls: Lists Docker images.
    StaticPromptSuggestion {
        name: "DOCKER_LIST_IMAGES",
        pattern: r"^docker\s+image\s+ls\s*$",
        label_template: None,
        query_template: "帮我管理 Docker 镜像。",
    },
    // docker-compose up -d <service>: Spins up a service <service> in Docker Compose.
    StaticPromptSuggestion {
        name: "DOCKER_COMPOSE_UP_SERVICE",
        pattern: r"^docker-compose\s+up\s+-d\s+(\S+)\s*$",
        label_template: Some("帮我使用 Docker Compose 管理或排查 {1}"),
        query_template: "帮我使用 Docker Compose 管理或排查 {1}。",
    },
    // docker network create <network>: Creates a Docker network named <network>.
    StaticPromptSuggestion {
        name: "DOCKER_NETWORK_CREATE",
        pattern: r"^docker\s+network\s+create\s+(\S+)\s*$",
        label_template: None,
        query_template: "帮我配置容器以使用 {1}。",
    },
    // vagrant init <box>: Initializes a Vagrant box named <box>.
    StaticPromptSuggestion {
        name: "VAGRANT_INIT_BOX",
        pattern: r"^vagrant\s+init\s+(\S+)\s*$",
        label_template: None,
        query_template: "帮我设置或自定义 Vagrant box {1}。",
    },
    // vagrant up: Brings up a Vagrant environment.
    StaticPromptSuggestion {
        name: "VAGRANT_UP",
        pattern: r"^vagrant\s+up\s*$",
        label_template: None,
        query_template: "帮我预配环境或排查 Vagrant 启动问题。",
    },
    // grep -r <pattern>: Searches recursively for <pattern> in files.
    StaticPromptSuggestion {
        // Capture everything after `grep -r ` into capture group 1.
        name: "GREP_RECURSIVE_SEARCH",
        pattern: r"^grep\s+-r\s+(.*)$",
        label_template: None,
        query_template: "帮我在多个文件中搜索 {1} 的代码。",
    },
    // find <args>: Searches for files/directories using `find`.
    StaticPromptSuggestion {
        // Capture everything after `find ` into capture group 1.
        // E.g. `find . -name "*.rs"`.
        name: "FIND_FILES",
        pattern: r"^find\s+(.*)$",
        label_template: None,
        query_template: "帮我使用 {1} 在多个文件中搜索代码。",
    },
    // ssh-keygen (no args): Generates an SSH key with default options.
    StaticPromptSuggestion {
        // This pattern matches "ssh-keygen" by itself or anything after it (e.g. "-t rsa -b 4096").
        name: "SSH_KEYGEN",
        pattern: r"^ssh-keygen(?:\s+(.*))?$",
        // We’ll keep the label/query generic so it applies whether or not the user passed extra flags.
        // Not using the capture group here, but it's there if we need it for the future.
        label_template: None,
        query_template: "带我生成一个 SSH 密钥。",
    },
];

pub fn apply_captures(template: &str, captures: &regex::Captures) -> String {
    // We'll look for placeholders of the form `{1}`, `{2}`, etc. and replace them with the
    // corresponding capture group.
    let mut result = String::from(template);

    for i in 1..captures.len() {
        let placeholder = format!("{{{i}}}");
        if let Some(m) = captures.get(i) {
            result = result.replace(&placeholder, m.as_str());
        }
    }
    result
}
