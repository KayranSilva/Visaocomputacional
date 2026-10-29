import colorsys
import copy
import random
import tkinter as tk
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from tkinter import ttk


BOARD_SIZE = 9
AGENT_COUNT = BOARD_SIZE * BOARD_SIZE
SIMILARITY_WEIGHTS = {
	"course": 4,
	"period": 3,
	"religion": 1,
	"state": 1,
	"gender": 1,
	"age": 1,
}
TOTAL_WEIGHT = sum(SIMILARITY_WEIGHTS.values())
COPYABLE_ATTRIBUTES = ("course", "religion")
ATTRIBUTE_LABELS = {
	"course": "Curso",
	"period": "Período",
	"religion": "Religião",
	"state": "Origem",
	"gender": "Sexo",
	"age": "Faixa etária",
	"graduated": "Situação acadêmica",
}

COURSES = (
	"Administração · Palmas",
	"Arquitetura e Urbanismo · Palmas",
	"Ciência da Computação · Palmas",
	"Enfermagem · Palmas",
	"Engenharia Ambiental · Palmas",
	

	
)

RELIGIONS = (
	"Catolicismo",
	"Evangelicalismo",
	"Espiritismo",
)

REGIONS = (
	"Norte",
    "Nordeste",
	"Centro-Oeste",
    "Sul",
    "Sudeste",

)

GENDERS = ("Masculino", "Feminino")
BACKGROUND = "#F2F5F3"
INK = "#20312F"
MUTED = "#61716E"
ACCENT = "#176B55"


def age_group(age: int) -> str:
	if age < 25:
		return "18–24"
	if age < 35:
		return "25–34"
	if age < 45:
		return "35–44"
	return "45+"


@dataclass
class Agent:
	identifier: int
	gender: str
	age: int
	period: int
	course: str
	religion: str
	state: str
	row: int
	column: int
	graduated: bool = False
	history: list[str] = field(default_factory=list)


def make_agents() -> list[Agent]:
	genders = list(GENDERS)
	genders.extend(random.choice(GENDERS) for _ in range(AGENT_COUNT - len(genders)))
	random.shuffle(genders)
	return [
		Agent(
			identifier=index + 1,
			gender=genders[index],
			age=random.randint(18, 60),
			period=random.randint(1, 8),
			course=random.choice(COURSES),
			religion=random.choice(RELIGIONS),
			state=random.choice(REGIONS),
			row=index // BOARD_SIZE,
			column=index % BOARD_SIZE,
		)
		for index in range(AGENT_COUNT)
	]


def similarity(first: Agent, second: Agent) -> float:
	matches = sum(
		weight
		for attribute, weight in SIMILARITY_WEIGHTS.items()
		if getattr(first, attribute) == getattr(second, attribute)
	)
	return matches / TOTAL_WEIGHT


def culture_color(agent: Agent) -> str:
	culture = (agent.gender, agent.period, agent.course, agent.religion, agent.state)
	hue = (hash(culture) % 360) / 360
	red, green, blue = colorsys.hsv_to_rgb(hue, 0.48, 0.88)
	return f"#{round(red * 255):02X}{round(green * 255):02X}{round(blue * 255):02X}"


def interact(source: Agent, neighbor: Agent) -> bool:
	if random.random() >= similarity(source, neighbor):
		return False

	different_attributes = [
		attribute
		for attribute in COPYABLE_ATTRIBUTES
		if getattr(source, attribute) != getattr(neighbor, attribute)
	]
	if not different_attributes:
		return False

	attribute = random.choices(
		different_attributes,
		weights=[SIMILARITY_WEIGHTS[item] for item in different_attributes],
		k=1,
	)[0]
	setattr(source, attribute, getattr(neighbor, attribute))
	return True


def has_copyable_difference(first: Agent, second: Agent) -> bool:
	return any(
		getattr(first, attribute) != getattr(second, attribute)
		for attribute in COPYABLE_ATTRIBUTES
	)


class SocialExperimentApp:
	cell_size = 58

	def __init__(self, root: tk.Tk) -> None:
		self.root = root
		self.root.title("Encontros | Difusão cultural")
		self.root.geometry("1180x980")
		self.root.minsize(1080, 900)
		self.root.configure(bg=BACKGROUND)
		self.agents = make_agents()
		self.original_agents = copy.deepcopy(self.agents)
		self.steps = 0
		self.interactions = 0
		self.change_counts: dict[str, Counter] = defaultdict(Counter)
		self.running = False
		self.show_original = False
		self.leader_id: int | None = None
		self.selected: Agent | None = None
		self.last_move = "População pronta. Inicie a difusão cultural."
		self.speed = tk.IntVar(value=220)
		self._elect_leader()
		self._configure_styles()
		self._build_interface()
		self._draw_board()
		self._update_dashboard()

	def _configure_styles(self) -> None:
		style = ttk.Style(self.root)
		style.theme_use("clam")
		style.configure("TFrame", background=BACKGROUND)
		style.configure("Panel.TFrame", background="#FFFFFF")
		style.configure("TLabel", background=BACKGROUND, foreground=INK, font=("TkDefaultFont", 10))
		style.configure("Panel.TLabel", background="#FFFFFF", foreground=INK, font=("TkDefaultFont", 10))
		style.configure("Title.TLabel", font=("TkDefaultFont", 23, "bold"))
		style.configure("Subtitle.TLabel", foreground=MUTED, font=("TkDefaultFont", 10))
		style.configure("Section.TLabel", background="#FFFFFF", font=("TkDefaultFont", 12, "bold"))
		style.configure("Metric.TLabel", background="#FFFFFF", foreground=ACCENT, font=("TkDefaultFont", 20, "bold"))
		style.configure("Primary.TButton", background=ACCENT, foreground="#FFFFFF", padding=(14, 9))
		style.map("Primary.TButton", background=[("active", "#105541")])

	def _add_legend_item(
		self, parent: ttk.Frame, symbol: str, text: str, color: str = INK
	) -> None:
		item = ttk.Frame(parent, style="Panel.TFrame")
		item.pack(side="left", padx=(0, 10))
		ttk.Label(item, text=symbol, style="Panel.TLabel", foreground=color).pack(side="left")
		ttk.Label(item, text=text, style="Panel.TLabel").pack(side="left", padx=(4, 0))

	def _build_interface(self) -> None:
		outer = ttk.Frame(self.root, padding=(24, 20))
		outer.pack(fill="both", expand=True)
		outer.columnconfigure(0, weight=1)
		outer.rowconfigure(1, weight=1)

		header = ttk.Frame(outer)
		header.grid(row=0, column=0, sticky="ew", pady=(0, 16))
		ttk.Label(header, text="ENCONTROS", style="Title.TLabel").pack(anchor="w")
		ttk.Label(
			header,
			text=f"{AGENT_COUNT} agentes. Seis características. Como as culturas se transformam?",
			style="Subtitle.TLabel",
		).pack(anchor="w", pady=(3, 0))

		body = ttk.Frame(outer)
		body.grid(row=1, column=0, sticky="nsew")
		body.columnconfigure(0, weight=3)
		body.columnconfigure(1, weight=2)
		body.rowconfigure(0, weight=1)

		board_panel = ttk.Frame(body, style="Panel.TFrame", padding=16)
		board_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
		board_panel.columnconfigure(0, weight=1)
		self.board_title = ttk.Label(
			board_panel,
			text=f"Tabuleiro {BOARD_SIZE} × {BOARD_SIZE} · {AGENT_COUNT} agentes",
			style="Section.TLabel",
		)
		self.board_title.grid(
			row=0, column=0, sticky="w", pady=(0, 12)
		)
		self.canvas = tk.Canvas(
			board_panel,
			width=BOARD_SIZE * self.cell_size,
			height=BOARD_SIZE * self.cell_size,
			bg="#FFFFFF",
			highlightthickness=0,
		)
		self.canvas.grid(row=1, column=0, sticky="n")
		self.canvas.bind("<Button-1>", self._select_cell)
		self.population_button = ttk.Button(
			board_panel,
			text="Ver população original",
			command=self._toggle_population_view,
		)
		self.population_button.grid(row=2, column=0, sticky="w", pady=(10, 0))
		legend = ttk.Frame(board_panel, style="Panel.TFrame")
		legend.grid(row=3, column=0, sticky="ew", pady=(12, 0))
		self._add_legend_item(legend, "M/F", "sexo")
		self._add_legend_item(legend, "●", "cor = cultura", "#527E70")
		self._add_legend_item(legend, "◎", "líder", "#D59B24")
		self._add_legend_item(legend, "□", "centro", ACCENT)
		ttk.Label(
			legend, text="Clique numa casa para ver detalhes", style="Panel.TLabel"
		).pack(side="left", padx=(4, 0))
		self.summary_frame = ttk.Frame(board_panel, style="Panel.TFrame")
		self.summary_frame.grid(row=4, column=0, sticky="nsew", pady=(16, 0))
		self.summary_frame.columnconfigure(0, weight=1)
		self.summary_frame.rowconfigure(1, weight=1)
		ttk.Label(
			self.summary_frame,
			text="Distribuição da população ao pausar",
			style="Section.TLabel",
		).grid(row=0, column=0, sticky="w", pady=(0, 6))
		summary_area = ttk.Frame(self.summary_frame, style="Panel.TFrame")
		summary_area.grid(row=1, column=0, sticky="nsew")
		summary_area.columnconfigure(0, weight=1)
		summary_area.rowconfigure(0, weight=1)
		self.summary_text = tk.Text(
			summary_area,
			height=9,
			wrap="word",
			font=("TkDefaultFont", 9),
			background="#F7F9F8",
			foreground=INK,
			borderwidth=0,
			state="disabled",
		)
		self.summary_text.grid(row=0, column=0, sticky="nsew")
		summary_scrollbar = ttk.Scrollbar(
			summary_area, orient="vertical", command=self.summary_text.yview
		)
		summary_scrollbar.grid(row=0, column=1, sticky="ns")
		self.summary_text.configure(yscrollcommand=summary_scrollbar.set)
		self.summary_frame.grid_remove()

		sidebar = ttk.Frame(body, style="Panel.TFrame", padding=18)
		sidebar.grid(row=0, column=1, sticky="nsew")
		sidebar.columnconfigure(0, weight=1)
		ttk.Label(sidebar, text="Simulação", style="Section.TLabel").grid(
			row=0, column=0, sticky="w"
		)
		controls = ttk.Frame(sidebar, style="Panel.TFrame")
		controls.grid(row=1, column=0, sticky="ew", pady=(10, 14))
		controls.columnconfigure((0, 1), weight=1)
		self.play_button = ttk.Button(
			controls, text="Iniciar", style="Primary.TButton", command=self._toggle_running
		)
		self.play_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
		ttk.Button(controls, text="Avançar", command=self._step).grid(
			row=0, column=1, sticky="ew", padx=(5, 0)
		)
		ttk.Button(sidebar, text="Nova população aleatória", command=self._reset).grid(
			row=2, column=0, sticky="ew"
		)
		ttk.Label(sidebar, text="Ritmo", style="Panel.TLabel").grid(
			row=3, column=0, sticky="w", pady=(16, 0)
		)
		ttk.Scale(sidebar, from_=80, to=700, variable=self.speed).grid(
			row=4, column=0, sticky="ew", pady=(4, 10)
		)

		metrics = ttk.Frame(sidebar, style="Panel.TFrame")
		metrics.grid(row=5, column=0, sticky="ew", pady=(2, 14))
		metrics.columnconfigure((0, 1, 2), weight=1)
		self.steps_label = ttk.Label(metrics, text="0", style="Metric.TLabel")
		self.steps_label.grid(row=0, column=0, sticky="w")
		self.interactions_label = ttk.Label(metrics, text="0", style="Metric.TLabel")
		self.interactions_label.grid(row=0, column=1, sticky="w")
		self.cultures_label = ttk.Label(metrics, text="0", style="Metric.TLabel")
		self.cultures_label.grid(row=0, column=2, sticky="w")
		ttk.Label(metrics, text="rodadas", style="Panel.TLabel").grid(row=1, column=0, sticky="w")
		ttk.Label(metrics, text="cópias", style="Panel.TLabel").grid(row=1, column=1, sticky="w")
		ttk.Label(metrics, text="culturas", style="Panel.TLabel").grid(row=1, column=2, sticky="w")

		self.status_label = ttk.Label(
			sidebar, text=self.last_move, style="Panel.TLabel", wraplength=330
		)
		self.status_label.grid(row=6, column=0, sticky="w", pady=(0, 10))
		ttk.Separator(sidebar).grid(row=7, column=0, sticky="ew", pady=(3, 14))
		ttk.Label(sidebar, text="Agente selecionado", style="Section.TLabel").grid(
			row=8, column=0, sticky="w", pady=(0, 8)
		)
		self.agent_details = ttk.Label(
			sidebar,
			text="Clique em uma casa para inspecionar o agente.",
			style="Panel.TLabel",
			justify="left",
			wraplength=330,
		)
		self.agent_details.grid(row=9, column=0, sticky="w")
		ttk.Separator(sidebar).grid(row=10, column=0, sticky="ew", pady=(14, 12))
		ttk.Label(sidebar, text="Histórico de mudanças", style="Section.TLabel").grid(
			row=11, column=0, sticky="w"
		)
		history_frame = ttk.Frame(sidebar, style="Panel.TFrame")
		history_frame.grid(row=12, column=0, sticky="nsew", pady=(6, 8))
		history_frame.columnconfigure(0, weight=1)
		history_frame.rowconfigure(0, weight=1)
		self.history_list = tk.Text(
			history_frame,
			height=5,
			width=38,
			wrap="word",
			font=("TkDefaultFont", 9),
			background="#F7F9F8",
			foreground=INK,
			borderwidth=0,
			state="disabled",
		)
		self.history_list.grid(row=0, column=0, sticky="nsew")
		history_scrollbar = ttk.Scrollbar(
			history_frame, orient="vertical", command=self.history_list.yview
		)
		history_scrollbar.grid(row=0, column=1, sticky="ns")
		self.history_list.configure(yscrollcommand=history_scrollbar.set)
		ttk.Separator(sidebar).grid(row=13, column=0, sticky="ew", pady=(8, 12))
		ttk.Label(sidebar, text="Regra de difusão", style="Section.TLabel").grid(
			row=14, column=0, sticky="w"
		)
		ttk.Label(
			sidebar,
			text="Líder: escolhido pela semelhança com vizinhos. A cada 50 rodadas, troca de "
			"lugar com o adjacente mais parecido entre os que o aproximam do centro. "
			"Contorno verde marca o destino; quando chega, permanece lá. "
			"A cada 50 rodadas, cada agente tem 5–8% de chance de copiar curso ou "
			"religião do líder. O líder não recebe cópias dos outros.\n"
			"Curso 4 · Período 3 · Religião 1 · Origem 1 · Sexo 1 · Idade 1\n"
			"Além disso, cada rodada sorteia um agente e um vizinho ortogonal: a chance "
			"de interação é a semelhança, e só curso ou religião podem ser copiados. "
			"Sexo e origem são fixos. A cada 500 rodadas, estudantes "
			"avançam um período até o 12º; na próxima progressão, formam-se. A idade "
			"aumenta a cada 1.000 rodadas. Idade e período não são copiados.",
			style="Panel.TLabel",
			wraplength=330,
			justify="left",
		).grid(row=15, column=0, sticky="w", pady=(6, 0))
		ttk.Label(
			outer,
			text=(
				"Idade sorteada entre 18 e 60 anos. Cursos de graduação da UFT por câmpus; "
				"sete religiões ilustrativas; "
				"26 estados e o Distrito Federal. Experimento didático, não previsão social."
			),
			style="Subtitle.TLabel",
		).grid(row=2, column=0, sticky="w", pady=(12, 0))

	def _draw_board(self) -> None:
		self.canvas.delete("all")
		for row in range(BOARD_SIZE):
			for column in range(BOARD_SIZE):
				left = column * self.cell_size
				top = row * self.cell_size
				is_center = row == BOARD_SIZE // 2 and column == BOARD_SIZE // 2
				self.canvas.create_rectangle(
					left,
					top,
					left + self.cell_size,
					top + self.cell_size,
					fill="#FFFFFF",
					outline=ACCENT if is_center else "#E0E7E3",
					width=3 if is_center else 1,
				)
		visible_agents = self.original_agents if self.show_original else self.agents
		for agent in visible_agents:
			left = agent.column * self.cell_size
			top = agent.row * self.cell_size
			selected = self.selected is not None and agent.identifier == self.selected.identifier
			is_leader = not self.show_original and agent.identifier == self.leader_id
			inset = 10 if selected else 14
			self.canvas.create_oval(
				left + inset,
				top + inset,
				left + self.cell_size - inset,
				top + self.cell_size - inset,
				fill=culture_color(agent),
				outline="#D59B24" if is_leader else "#173D39" if selected else "",
				width=4 if is_leader else 3 if selected else 1,
			)
			self.canvas.create_text(
				left + self.cell_size / 2,
				top + self.cell_size / 2,
				text="M" if agent.gender == "Masculino" else "F",
				fill=INK,
				font=("TkDefaultFont", 9, "bold"),
			)

	def _select_cell(self, event: tk.Event) -> None:
		column = min(event.x // self.cell_size, BOARD_SIZE - 1)
		row = min(event.y // self.cell_size, BOARD_SIZE - 1)
		visible_agents = self.original_agents if self.show_original else self.agents
		self.selected = next(
			agent for agent in visible_agents if agent.row == row and agent.column == column
		)
		self._draw_board()
		self._update_dashboard()

	def _toggle_population_view(self) -> None:
		self.show_original = not self.show_original
		visible_agents = self.original_agents if self.show_original else self.agents
		if self.selected is not None:
			self.selected = visible_agents[self.selected.identifier - 1]
		self.population_button.configure(
			text="Mostrar população atual" if self.show_original else "Ver população original"
		)
		view_name = "População original" if self.show_original else "População atual"
		self.board_title.configure(
			text=f"{view_name} · {BOARD_SIZE} × {BOARD_SIZE} · {AGENT_COUNT} agentes"
		)
		self._draw_board()
		self._update_dashboard()

	def _neighbors_of(self, agent: Agent) -> list[Agent]:
		return [
			candidate
			for candidate in self.agents
			if abs(candidate.row - agent.row) + abs(candidate.column - agent.column) == 1
		]

	def _distance_to_center(self, agent: Agent) -> int:
		center = BOARD_SIZE // 2
		return abs(agent.row - center) + abs(agent.column - center)

	def _move_leader_toward_center(self, leader: Agent) -> str:
		current_distance = self._distance_to_center(leader)
		if current_distance == 0:
			return f"Líder {leader.identifier} chegou ao centro e permanece lá."

		candidates = [
			neighbor
			for neighbor in self._neighbors_of(leader)
			if self._distance_to_center(neighbor) < current_distance
		]
		best_similarity = max(similarity(leader, candidate) for candidate in candidates)
		best_candidates = [
			candidate
			for candidate in candidates
			if similarity(leader, candidate) == best_similarity
		]
		destination = random.choice(best_candidates)
		old_position = (leader.row, leader.column)
		leader.row, destination.row = destination.row, leader.row
		leader.column, destination.column = destination.column, leader.column
		movement = (
			f"Líder {leader.identifier} avançou de {old_position} para "
			f"({leader.row}, {leader.column}), trocando com o adjacente mais "
			f"semelhante ({best_similarity:.0%})."
		)
		leader.history.append(f"R{self.steps} · {movement}")
		return movement

	def _leader_score(self, agent: Agent) -> float:
		return sum(similarity(agent, neighbor) for neighbor in self._neighbors_of(agent))

	def _elect_leader(self) -> Agent:
		scores = {agent.identifier: self._leader_score(agent) for agent in self.agents}
		highest_score = max(scores.values())
		candidates = [
			agent for agent in self.agents if scores[agent.identifier] == highest_score
		]
		leader = random.choice(candidates)
		self.leader_id = leader.identifier
		return leader

	def _leader_influence(self, leader: Agent) -> list[str]:
		changes = []
		for agent in self.agents:
			if agent is leader or random.random() >= random.uniform(0.05, 0.08):
				continue
			different_attributes = [
				attribute
				for attribute in COPYABLE_ATTRIBUTES
				if getattr(agent, attribute) != getattr(leader, attribute)
			]
			if not different_attributes:
				continue
			attribute = random.choice(different_attributes)
			previous_value = getattr(agent, attribute)
			new_value = getattr(leader, attribute)
			setattr(agent, attribute, new_value)
			self.interactions += 1
			self.change_counts[attribute][new_value] += 1
			agent.history.append(
				f"R{self.steps} · {ATTRIBUTE_LABELS[attribute]}: "
				f"{previous_value} → {new_value} · líder {leader.identifier} "
				"(influência de período)"
			)
			changes.append(
				f"agente {agent.identifier} mudou {ATTRIBUTE_LABELS[attribute].lower()}"
			)
		return changes

	def _is_stable(self) -> bool:
		for agent in self.agents:
			neighbors = [
				neighbor
				for neighbor in self._neighbors_of(agent)
				if neighbor.row > agent.row
				or (neighbor.row == agent.row and neighbor.column > agent.column)
			]
			if any(
				0 < similarity(agent, neighbor) < 1
				and has_copyable_difference(agent, neighbor)
				for neighbor in neighbors
			):
				return False
		return True

	def _is_complete(self) -> bool:
		leader = next(agent for agent in self.agents if agent.identifier == self.leader_id)
		return (
			self._is_stable()
			and all(agent.graduated for agent in self.agents)
			and self._distance_to_center(leader) == 0
		)

	def _advance_life_stages(self) -> None:
		if self.steps % 500 == 0:
			for agent in self.agents:
				if agent.graduated:
					continue
				if agent.period < 12:
					previous_period = agent.period
					agent.period += 1
					self.change_counts["period"][agent.period] += 1
					agent.history.append(
						f"R{self.steps} · Período: {previous_period}º → {agent.period}º"
					)
				else:
					agent.graduated = True
					self.change_counts["graduated"]["Formado"] += 1
					agent.history.append(
						f"R{self.steps} · Concluiu o 12º período · Formado"
					)

		if self.steps % 50 == 0:
			leader = next(agent for agent in self.agents if agent.identifier == self.leader_id)
			movement = self._move_leader_toward_center(leader)
			leader_changes = self._leader_influence(leader)
			if leader_changes:
				self.last_move = (
					f"Rodada {self.steps}: {movement} " + "; ".join(leader_changes)
				)
			else:
				self.last_move = (
					f"Rodada {self.steps}: {movement} "
					"Nenhum agente adotou uma característica nesta influência."
				)

		if self.steps % 1000 == 0:
			for agent in self.agents:
				previous_age = agent.age
				agent.age += 1
				self.change_counts["age"][age_group(agent.age)] += 1
				agent.history.append(
					f"R{self.steps} · Idade: {previous_age} → {agent.age} anos"
				)

	def _step(self) -> None:
		if self._is_complete():
			self._finish_stable()
			self._update_dashboard()
			return
		source = random.choice(self.agents)
		neighbor = random.choice(self._neighbors_of(source))
		self.steps += 1
		previous_values = {
			attribute: getattr(source, attribute)
			for attribute in COPYABLE_ATTRIBUTES
		}
		if source.identifier != self.leader_id and interact(source, neighbor):
			self.interactions += 1
			changed_attribute = next(
				attribute
				for attribute in COPYABLE_ATTRIBUTES
				if getattr(source, attribute) != previous_values[attribute]
			)
			self.change_counts[changed_attribute][getattr(source, changed_attribute)] += 1
			source.history.append(
				f"R{self.steps} · {ATTRIBUTE_LABELS[changed_attribute]}: "
				f"{previous_values[changed_attribute]} → {getattr(source, changed_attribute)} "
				f"· agente {neighbor.identifier}"
			)
			self.last_move = (
				f"Rodada {self.steps}: agente {source.identifier} adotou uma característica "
				f"do vizinho {neighbor.identifier}."
			)
		else:
			self.last_move = f"Rodada {self.steps}: sem mudança cultural neste par."
		self._advance_life_stages()
		if self._is_complete():
			self._finish_stable()
		self._draw_board()
		self._update_dashboard()

	def _finish_stable(self) -> None:
		self.running = False
		self.last_move = "Culturas estáveis e todos os agentes formados. Experimento concluído."
		self.play_button.configure(text="Iniciar")
		self._show_population_summary()

	def _update_dashboard(self) -> None:
		self.steps_label.configure(text=str(self.steps))
		self.interactions_label.configure(text=str(self.interactions))
		cultures = {
			(agent.gender, agent.period, agent.course, agent.religion, agent.state)
			for agent in self.agents
		}
		self.cultures_label.configure(text=str(len(cultures)))
		self.status_label.configure(text=self.last_move)
		if self.selected is None:
			self.agent_details.configure(text="Clique em uma casa para inspecionar o agente.")
			self.history_list.configure(state="normal")
			self.history_list.delete("1.0", tk.END)
			self.history_list.insert("1.0", "Selecione um agente para ver o histórico.")
			self.history_list.configure(state="disabled")
			return
		agent = self.selected
		self.agent_details.configure(
			text=(
				f"Agente {agent.identifier:02d}\n"
				f"Sexo: {agent.gender}\n"
				f"Idade: {agent.age} anos\n"
				f"Período: {agent.period}º\n"
				f"Situação: {'Formado' if agent.graduated else 'Estudante'}\n"
				f"Papel: {'Líder local' if not self.show_original and agent.identifier == self.leader_id else 'Agente'}\n"
				f"Casa: linha {agent.row + 1}, coluna {agent.column + 1}\n"
				f"Curso: {agent.course}\n"
				f"Religião: {agent.religion}\n"
				f"Origem: {agent.state}"
			)
		)
		self.history_list.configure(state="normal")
		self.history_list.delete("1.0", tk.END)
		if not agent.history:
			self.history_list.insert("1.0", "Nenhuma mudança registrada.")
		else:
			self.history_list.insert("1.0", "\n".join(reversed(agent.history)))
		self.history_list.configure(state="disabled")

	def _show_population_summary(self) -> None:
		lines = [
			f"Resumo após {self.steps} rodadas · {self.interactions} mudanças realizadas",
			"Valores mais frequentes na população:",
		]
		for attribute in ("course", "religion"):
			current_counts = Counter(getattr(agent, attribute) for agent in self.agents)
			maximum = max(current_counts.values())
			leaders = sorted(
				value for value, count in current_counts.items() if count == maximum
			)
			label = ATTRIBUTE_LABELS[attribute]
			tie_label = " (empate)" if len(leaders) > 1 else ""
			lines.append(f"\n{label} mais frequente{tie_label}:")
			for value in leaders:
				adoptions = self.change_counts[attribute][value]
				lines.append(
					f"  {value} · {maximum} de {len(self.agents)} agentes · "
					f"adotado {adoptions} vez(es)"
				)
		self.summary_text.configure(state="normal")
		self.summary_text.delete("1.0", tk.END)
		self.summary_text.insert("1.0", "\n".join(lines))
		self.summary_text.configure(state="disabled")
		self.summary_frame.grid()

	def _toggle_running(self) -> None:
		if self.running:
			self.running = False
			self.play_button.configure(text="Iniciar")
			self.last_move = "Simulação pausada. Resumo da população atualizado."
			self._show_population_summary()
			self._update_dashboard()
			return

		if not self.running and self._is_complete():
			self._finish_stable()
			self._update_dashboard()
			return
		self.summary_frame.grid_remove()
		self.running = True
		self.play_button.configure(text="Pausar")
		self._schedule_step()

	def _schedule_step(self) -> None:
		if self.running:
			self._step()
			if self.running:
				self.root.after(max(40, self.speed.get()), self._schedule_step)

	def _reset(self) -> None:
		self.running = False
		self.play_button.configure(text="Iniciar")
		self.agents = make_agents()
		self.original_agents = copy.deepcopy(self.agents)
		self.steps = 0
		self.interactions = 0
		self.change_counts = defaultdict(Counter)
		self.selected = None
		self.show_original = False
		self._elect_leader()
		self.population_button.configure(text="Ver população original")
		self.board_title.configure(
			text=f"Tabuleiro {BOARD_SIZE} × {BOARD_SIZE} · {AGENT_COUNT} agentes"
		)
		self.last_move = "Nova população sorteada. Inicie a difusão cultural."
		self.summary_frame.grid_remove()
		self._draw_board()
		self._update_dashboard()


def main() -> None:
	root = tk.Tk()
	SocialExperimentApp(root)
	root.mainloop()


if __name__ == "__main__":
	main()
