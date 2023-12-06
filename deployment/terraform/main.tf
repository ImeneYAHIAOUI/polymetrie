terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = ">= 2.0.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "polymetrie-increment" {
  metadata {
    name = "polymetrie-increment"
  }
}

resource "kubernetes_deployment" "polymetrie-increment" {
  metadata {
    name = "polymetrie-increment"
    namespace = kubernetes_namespace.polymetrie-increment.metadata[0].name
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "polymetrie-increment"
      }
    }
    template {
      metadata {
        labels = {
          app = "polymetrie-increment"
        }
      }
      spec {
        container {
          name = "polymetrie-increment"
          image = "hamza125/polymetrie-increment:latest"
          port {
            container_port = 5000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "polymetrie-increment" {
  metadata {
    name = "polymetrie-increment-service"
    namespace = kubernetes_namespace.polymetrie-increment.metadata[0].name
  }

  spec {
    selector = {
      app = "polymetrie-increment"
    }
    port {
      protocol = "TCP"
      port = 5000
      target_port = 5000
    }
  }
}

resource "kubernetes_ingress" "polymetrie-increment" {
  metadata {
    name = "polymetrie-increment-ingress"
    namespace = kubernetes_namespace.polymetrie-increment.metadata[0].name
  }

  spec {
    rule {
      host = "polymetrie-increment.com"
      http {
        path {
          path = "/"
          backend {
            service_name = kubernetes_service.polymetrie-increment.metadata[0].name
            service_port = kubernetes_service.polymetrie-increment.spec[0].port[0].port
          }
        }
      }
    }
  }
}

