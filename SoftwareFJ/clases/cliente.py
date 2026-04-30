class Cliente:
    def __init__(self, id_cliente, nombre, edad, correo):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.edad = edad
        self.correo = correo

    def __str__(self):
        return f"[{self.id_cliente}] {self.nombre} - {self.edad} años - {self.correo}"

        from clases.cliente import Cliente


class SistemaClientes:
    def __init__(self):
        self.clientes = []

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)
        print("✅ Cliente agregado")

    def listar_clientes(self):
        if not self.clientes:
            print("⚠️ No hay clientes registrados")
            return
        for cliente in self.clientes:
            print(cliente)

    def buscar_cliente(self, id_cliente):
        for cliente in self.clientes:
            if cliente.id_cliente == id_cliente:
                return cliente
        return None

    def actualizar_cliente(self, id_cliente, nombre=None, edad=None, correo=None):
        cliente = self.buscar_cliente(id_cliente)
        if cliente:
            if nombre:
                cliente.nombre = nombre
            if edad:
                cliente.edad = edad
            if correo:
                cliente.correo = correo
            print("🔄 Cliente actualizado")
        else:
            print("❌ Cliente no encontrado")

    def eliminar_cliente(self, id_cliente):
        cliente = self.buscar_cliente(id_cliente)
        if cliente:
            self.clientes.remove(cliente)
            print("🗑️ Cliente eliminado")
        else:
            print("❌ Cliente no encontrado")


# 🚀 PRUEBA
if __name__ == "__main__":
    sistema = SistemaClientes()

    c1 = Cliente(1, "Juan", 25, "juan@gmail.com")
    c2 = Cliente(2, "Maria", 30, "maria@gmail.com")

    sistema.agregar_cliente(c1)
    sistema.agregar_cliente(c2)

    print("\n📋 Lista de clientes:")
    sistema.listar_clientes()

    print("\n🔍 Buscar cliente ID 1:")
    print(sistema.buscar_cliente(1))

    print("\n✏️ Actualizar cliente ID 2:")
    sistema.actualizar_cliente(2, nombre="Maria Lopez")

    print("\n📋 Lista actualizada:")
    sistema.listar_clientes()

    print("\n🗑️ Eliminar cliente ID 1:")
    sistema.eliminar_cliente(1)

    print("\n📋 Lista final:")
    sistema.listar_clientes()
    